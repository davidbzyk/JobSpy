from __future__ import annotations

import logging
import re
from itertools import cycle
from typing import Iterable

import numpy as np
import requests
import tls_client
import urllib3
from markdownify import markdownify as md
from requests.adapters import HTTPAdapter, Retry

from jobspy.model import CompensationInterval, JobType, Site
from jobspy.user_agents import get_default_user_agents

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RotatingProxySession:
    def __init__(self, proxies=None):
        if isinstance(proxies, str):
            self.proxy_cycle = cycle([self.format_proxy(proxies)])
        elif isinstance(proxies, list):
            self.proxy_cycle = (
                cycle([self.format_proxy(proxy) for proxy in proxies])
                if proxies
                else None
            )
        else:
            self.proxy_cycle = None

    @staticmethod
    def format_proxy(proxy):
        """Utility method to format a proxy string into a dictionary."""
        if proxy.startswith("http://") or proxy.startswith("https://"):
            return {"http": proxy, "https": proxy}
        if proxy.startswith("socks5://"):
            return {"http": proxy, "https": proxy}
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}


class RotatingUserAgent:
    def __init__(self, user_agents: Iterable[str] | None = None):
        if user_agents is None:
            user_agents = get_default_user_agents()
        elif isinstance(user_agents, str):
            user_agents = [user_agents]
        self.user_agent_cycle = cycle(user_agents)

    def get_user_agent(self) -> str:
        return next(self.user_agent_cycle)


class RequestsRotating(RotatingProxySession, RotatingUserAgent, requests.Session):
    def __init__(
        self,
        proxies=None,
        has_retry=False,
        delay=1,
        clear_cookies=False,
        user_agents=None,
    ):
        RotatingProxySession.__init__(self, proxies=proxies)
        RotatingUserAgent.__init__(self, user_agents=user_agents)
        requests.Session.__init__(self)
        self.clear_cookies = clear_cookies
        self.allow_redirects = True
        self.setup_session(has_retry, delay)

    def setup_session(self, has_retry, delay):
        if has_retry:
            retries = Retry(
                total=3,
                connect=3,
                status=3,
                status_forcelist=[500, 502, 503, 504, 429],
                backoff_factor=delay,
            )
            adapter = HTTPAdapter(max_retries=retries)
            self.mount("http://", adapter)
            self.mount("https://", adapter)

    def request(self, method, url, **kwargs):
        if self.clear_cookies:
            self.cookies.clear()

        if self.proxy_cycle:
            next_proxy = next(self.proxy_cycle)
            if next_proxy["http"] != "http://localhost":
                self.proxies = next_proxy
            else:
                self.proxies = {}
        headers = kwargs.get("headers", {})
        if "user-agent" not in headers:
            headers["user-agent"] = self.get_user_agent()
            kwargs["headers"] = headers
        return requests.Session.request(self, method, url, **kwargs)


class TLSRotating(RotatingProxySession, RotatingUserAgent, tls_client.Session):
    def __init__(self, proxies=None, user_agents=None, client_identifier="chrome_120"):
        RotatingProxySession.__init__(self, proxies=proxies)
        RotatingUserAgent.__init__(self, user_agents=user_agents)
        tls_client.Session.__init__(
            self,
            random_tls_extension_order=True,
            client_identifier=client_identifier,
        )
        self.logger = create_logger("TLSSession")

    def execute_request(self, *args, **kwargs):
        if self.proxy_cycle:
            next_proxy = next(self.proxy_cycle)
            if next_proxy["http"] != "http://localhost":
                self.proxies = next_proxy
                self.logger.info(f"Using proxy: {self.proxies.get('http')}")
            else:
                self.proxies = {}
        headers = kwargs.get("headers", {})
        if "user-agent" not in headers:
            headers["user-agent"] = self.get_user_agent()
            kwargs["headers"] = headers
        
        # Debug logging - check if args has the expected elements
        if len(args) >= 2:
            self.logger.debug(f"Requesting {args[0]} {args[1]} with headers: {headers}")
        else:
            self.logger.debug(f"Requesting with args: {args} and headers: {headers}")
        
        response = tls_client.Session.execute_request(self, *args, **kwargs)
        response.ok = response.status_code in range(200, 400)
        return response


def create_session(
    *,
    proxies: dict | str | None = None,
    ca_cert: str | None = None,
    is_tls: bool = True,
    has_retry: bool = False,
    delay: int = 1,
    clear_cookies: bool = False,
    user_agents: Iterable[str] | str | None = None,
    client_identifier: str | None = None,
) -> requests.Session:
    """
    Creates a requests session with optional tls, proxy, and retry settings.
    :return: A session object
    """
    if is_tls:
        session = TLSRotating(
            proxies=proxies,
            user_agents=user_agents,
            client_identifier=client_identifier or "chrome_120",
        )
    else:
        session = RequestsRotating(
            proxies=proxies,
            has_retry=has_retry,
            delay=delay,
            clear_cookies=clear_cookies,
            user_agents=user_agents,
        )

    if ca_cert:
        session.verify = ca_cert

    return session


def create_logger(name: str) -> logging.Logger:
    """Creates a logger with the given name."""
    return logging.getLogger(f"JobSpy:{name}")


def set_logger_level(verbose: int):
    """
    Adjusts the logger's level. This function allows the logging level to be changed at runtime.

    Parameters:
    - verbose: int {0, 1, 2} (0: warnings, 1: info, 2: debug)
    """
    if verbose is None:
        return
    level_name = {2: "DEBUG", 1: "INFO", 0: "WARNING"}.get(verbose, "INFO")
    level = getattr(logging, level_name.upper(), logging.INFO)

    root_logger = logging.getLogger("JobSpy")
    root_logger.setLevel(level)
    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

def markdown_converter(description_html: str):
    if description_html is None:
        return None
    markdown = md(description_html)
    return markdown.strip()


def extract_emails_from_text(text: str) -> list[str] | None:
    if not text:
        return None
    email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    return email_regex.findall(text)


def get_enum_from_job_type(job_type_str: str) -> JobType | None:
    """
    Given a string, returns the corresponding JobType enum member if a match is found.
    """
    res = None
    for job_type in JobType:
        if job_type_str in job_type.value:
            res = job_type
    return res


def currency_parser(cur_str):
    # Remove any non-numerical characters
    # except for ',' '.' or '-' (e.g. EUR)
    cur_str = re.sub("[^-0-9.,]", "", cur_str)
    # Remove any 000s separators (either , or .)
    cur_str = re.sub("[.,]", "", cur_str[:-3]) + cur_str[-3:]

    if "." in list(cur_str[-3:]):
        num = float(cur_str)
    elif "," in list(cur_str[-3:]):
        num = float(cur_str.replace(",", "."))
    else:
        num = float(cur_str)

    return np.round(num, 2)


def _parse_salary_value(value_str: str, k_suffix: str) -> int:
    """Helper to parse salary value and apply 'k' multiplier."""
    value = int(float(value_str.replace(",", "")))
    if "k" in k_suffix.lower():
        value *= 1000
    return value


def remove_attributes(tag):
    for attr in list(tag.attrs):
        del tag[attr]
    return tag


def extract_salary(
    salary_str: str | None,
    lower_limit: int = 1000,
    upper_limit: int = 700000,
    hourly_threshold: int = 350,
    monthly_threshold: int = 30000,
    enforce_annual_salary: bool = False,
) -> tuple[str | None, int | None, int | None, str | None]:
    """
    Extracts salary information from a string and returns the salary interval, min and max salary values, and currency.
    (TODO: Needs test cases as the regex is complicated)
    """
    if not salary_str:
        return None, None, None, None

    min_max_pattern = r"\$(\d+(?:,\d+)?(?:\.\d+)?)([kK]?)\s*[-—–]\s*(?:\$)?(\d+(?:,\d+)?(?:\.\d+)?)([kK]?)"
    match = re.search(min_max_pattern, salary_str)

    if not match:
        return None, None, None, None

    min_salary = _parse_salary_value(match.group(1), match.group(2))
    max_salary = _parse_salary_value(match.group(3), match.group(4))

    # Determine interval and calculate annual equivalents
    if min_salary < hourly_threshold and max_salary < hourly_threshold:
        interval = CompensationInterval.HOURLY.value
        annual_min = min_salary * 2080
        annual_max = max_salary * 2080
    elif min_salary < monthly_threshold and max_salary < monthly_threshold:
        interval = CompensationInterval.MONTHLY.value
        annual_min = min_salary * 12
        annual_max = max_salary * 12
    else:
        interval = CompensationInterval.YEARLY.value
        annual_min = min_salary
        annual_max = max_salary

    # Validate the calculated annual salary range
    is_valid_range = (
        lower_limit <= annual_min <= upper_limit
        and lower_limit <= annual_max <= upper_limit
        and annual_min < annual_max
    )

    if not is_valid_range:
        return None, None, None, None

    if enforce_annual_salary:
        return interval, annual_min, annual_max, "USD"
    else:
        return interval, min_salary, max_salary, "USD"


def extract_job_type(description: str):
    if not description:
        return []

    keywords = {
        JobType.FULL_TIME: r"full\s?time",
        JobType.PART_TIME: r"part\s?time",
        JobType.INTERNSHIP: r"internship",
        JobType.CONTRACT: r"contract",
    }

    listing_types = []
    for key, pattern in keywords.items():
        if re.search(pattern, description, re.IGNORECASE):
            listing_types.append(key)

    return listing_types


def map_str_to_site(site_name: str) -> Site:
    """Converts a string to a Site enum member, handling spaces."""
    processed_name = site_name.replace(" ", "_").upper()
    try:
        return Site[processed_name]
    except KeyError:
        raise ValueError(f"Invalid site name: '{site_name}'") from None


def get_enum_from_value(value_str):
    for job_type in JobType:
        if value_str in job_type.value:
            return job_type
    raise ValueError(f"Invalid job type: {value_str}")


def convert_to_annual(job_data: dict):
    if job_data["interval"] == "hourly":
        job_data["min_amount"] *= 2080
        job_data["max_amount"] *= 2080
    if job_data["interval"] == "monthly":
        job_data["min_amount"] *= 12
        job_data["max_amount"] *= 12
    if job_data["interval"] == "weekly":
        job_data["min_amount"] *= 52
        job_data["max_amount"] *= 52
    if job_data["interval"] == "daily":
        job_data["min_amount"] *= 260
        job_data["max_amount"] *= 260
    job_data["interval"] = "yearly"


DESIRED_ORDER = [
    "id",
    "site",
    "job_url",
    "job_url_direct",
    "title",
    "company",
    "location",
    "date_posted",
    "job_type",
    "salary_source",
    "interval",
    "min_amount",
    "max_amount",
    "currency",
    "is_remote",
    "job_level",
    "job_function",
    "listing_type",
    "emails",
    "description",
    "company_industry",
    "company_url",
    "company_logo",
    "company_url_direct",
    "company_addresses",
    "company_num_employees",
    "company_revenue",
    "company_description",
    # naukri-specific fields
    "skills",
    "experience_range",
    "company_rating",
    "company_reviews_count",
    "vacancy_count",
    "work_from_home_type",
]
