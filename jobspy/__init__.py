from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple

import pandas as pd

from jobspy.bayt import BaytScraper
from jobspy.glassdoor import Glassdoor
from jobspy.google import Google
from jobspy.indeed import Indeed
from jobspy.linkedin import LinkedIn
from jobspy.linkedin import LinkedIn
from jobspy.naukri import Naukri
from jobspy.model import JobType, Location, JobResponse, Country, JobPost
from jobspy.model import SalarySource, ScraperInput, Site
from jobspy.util import (
    set_logger_level,
    extract_salary,
    create_logger,
    get_enum_from_value,
    map_str_to_site,
    convert_to_annual,
    DESIRED_ORDER,
)
from jobspy.ziprecruiter import ZipRecruiter


def _process_job_data(
    job: JobPost,
    site: str,
    country_enum: Country,
    enforce_annual_salary: bool,
) -> dict:
    """Helper function to process a single job post into a dictionary for the DataFrame."""
    job_data = job.dict()
    job_data["site"] = site
    job_data["company"] = job_data["company_name"]
    job_data["job_type"] = (
        ", ".join(job_type.value[0] for job_type in job_data["job_type"])
        if job_data["job_type"]
        else None
    )
    job_data["emails"] = ", ".join(job_data["emails"]) if job_data["emails"] else None
    if job_data["location"]:
        job_data["location"] = Location(**job_data["location"]).display_location()

    # Handle compensation
    compensation_obj = job_data.get("compensation")
    if compensation_obj and isinstance(compensation_obj, dict):
        job_data["interval"] = (
            compensation_obj.get("interval").value
            if compensation_obj.get("interval")
            else None
        )
        job_data["min_amount"] = compensation_obj.get("min_amount")
        job_data["max_amount"] = compensation_obj.get("max_amount")
        job_data["currency"] = compensation_obj.get("currency", "USD")
        job_data["salary_source"] = SalarySource.DIRECT_DATA.value
        if enforce_annual_salary and (
            job_data["interval"]
            and job_data["interval"] != "yearly"
            and job_data["min_amount"]
            and job_data["max_amount"]
        ):
            convert_to_annual(job_data)
    else:
        if country_enum == Country.USA:
            (
                job_data["interval"],
                job_data["min_amount"],
                job_data["max_amount"],
                job_data["currency"],
            ) = extract_salary(
                job_data["description"],
                enforce_annual_salary=enforce_annual_salary,
            )
            job_data["salary_source"] = SalarySource.DESCRIPTION.value

    job_data["salary_source"] = (
        job_data["salary_source"]
        if "min_amount" in job_data and job_data["min_amount"]
        else None
    )

    job_data["skills"] = ", ".join(job_data["skills"]) if job_data["skills"] else None
    return job_data


def scrape_jobs(
    site_name: str | list[str] | Site | list[Site] | None = None,
    search_term: str | None = None,
    google_search_term: str | None = None,
    location: str | None = None,
    distance: int | None = 50,
    is_remote: bool = False,
    job_type: str | None = None,
    easy_apply: bool | None = None,
    results_wanted: int = 15,
    country_indeed: str = "usa",
    proxies: list[str] | str | None = None,
    ca_cert: str | None = None,
    description_format: str = "markdown",
    linkedin_fetch_description: bool | None = False,
    linkedin_company_ids: list[int] | None = None,
    offset: int | None = 0,
    hours_old: int = None,
    enforce_annual_salary: bool = False,
    verbose: int = 0,
    **kwargs,
) -> pd.DataFrame:
    """
    Scrapes job data from job boards concurrently
    :return: Pandas DataFrame containing job data
    """
    SCRAPER_MAPPING = {
        Site.LINKEDIN: LinkedIn,
        Site.INDEED: Indeed,
        Site.ZIP_RECRUITER: ZipRecruiter,
        Site.GLASSDOOR: Glassdoor,
        Site.GOOGLE: Google,
        Site.BAYT: BaytScraper,
        Site.NAUKRI: Naukri,
    }
    set_logger_level(verbose)
    job_type = get_enum_from_value(job_type) if job_type else None

    def get_site_type():
        site_types = list(Site)
        if isinstance(site_name, str):
            site_types = [map_str_to_site(site_name)]
        elif isinstance(site_name, Site):
            site_types = [site_name]
        elif isinstance(site_name, list):
            site_types = [
                map_str_to_site(site) if isinstance(site, str) else site
                for site in site_name
            ]
        return site_types

    country_enum = Country.from_string(country_indeed)

    scraper_input = ScraperInput(
        site_type=get_site_type(),
        country=country_enum,
        search_term=search_term,
        google_search_term=google_search_term,
        location=location,
        distance=distance,
        is_remote=is_remote,
        job_type=job_type,
        easy_apply=easy_apply,
        description_format=description_format,
        linkedin_fetch_description=linkedin_fetch_description,
        results_wanted=results_wanted,
        linkedin_company_ids=linkedin_company_ids,
        offset=offset,
        hours_old=hours_old,
        is_tls=kwargs.get("is_tls", False),
    )

    def scrape_site(site: Site) -> Tuple[str, JobResponse]:
        scraper_class = SCRAPER_MAPPING[site]
        scraper = scraper_class(proxies=proxies, ca_cert=ca_cert)
        scraped_data: JobResponse = scraper.scrape(scraper_input)
        cap_name = site.value.capitalize()
        site_name = "ZipRecruiter" if cap_name == "Zip_recruiter" else cap_name
        create_logger(site_name).info(f"finished scraping")
        return site.value, scraped_data

    site_to_jobs_dict = {}

    def worker(site):
        site_val, scraped_info = scrape_site(site)
        return site_val, scraped_info

    with ThreadPoolExecutor() as executor:
        future_to_site = {
            executor.submit(worker, site): site for site in scraper_input.site_type
        }

        for future in as_completed(future_to_site):
            site = future_to_site[future]
            try:
                site_value, scraped_data = future.result()
                site_to_jobs_dict[site_value] = scraped_data
            except Exception as e:
                create_logger(site.value).error(f"Failed to scrape site: {e}")

    processed_jobs: list[dict] = []

    for site, job_response in site_to_jobs_dict.items():
        for job in job_response.jobs:
            job_data = _process_job_data(
                job, site, country_enum, enforce_annual_salary
            )
            processed_jobs.append(job_data)

    if processed_jobs:
        jobs_df = pd.DataFrame(processed_jobs)

        # Ensure all desired columns are present, adding missing ones as empty
        for column in DESIRED_ORDER:
            if column not in jobs_df.columns:
                jobs_df[column] = None  # Add missing columns as empty

        # Reorder the DataFrame according to the desired order
        jobs_df = jobs_df[DESIRED_ORDER]

        return jobs_df.sort_values(
            by=["site", "date_posted"], ascending=[True, False]
        ).reset_index(drop=True)
    else:
        return pd.DataFrame()