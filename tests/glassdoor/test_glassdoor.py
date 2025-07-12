"""
Issues Fixed:
Tuple index out of range error in jobspy/util.py (line 123):
The code was trying to access args[0] and args[1] without checking if they existed
Fixed: Added bounds checking before accessing tuple elements
Missing raise_for_status() method in jobspy/glassdoor/__init__.py (line 277):
The TLS client response object doesn't have the raise_for_status() method that regular requests objects have
Fixed: Replaced with manual status code checking
"""


import logging
import sys
import os
import csv

# Add the project root to the Python path to allow for absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from jobspy import scrape_jobs

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()


if __name__ == "__main__":
    # Parameters to plug and play
    search_params = {
        "site_name": ["glassdoor"],
        "search_term": "Software Engineer",
        "location": "Miami, FL",
        "results_wanted": 20,
        "country_indeed": "USA"  # Glassdoor uses the same country param as Indeed
    }

    # Construct proxy string from environment variables for a paid proxy service
    proxy_host = os.getenv("PROXY_HOST")
    proxy_port = os.getenv("PROXY_PORT")
    proxy_user = os.getenv("PROXY_USER")
    proxy_pass = os.getenv("PROXY_PASS")

    proxy_list = []
    if all([proxy_host, proxy_port, proxy_user, proxy_pass]):
        proxy = f"{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        proxy_list.append(proxy)
        log.info(f"Using paid proxy: {proxy_host}:{proxy_port}")
    else:
        log.error("Paid proxy environment variables not set. Glassdoor requires a proxy. Exiting.")
        exit(1)

    log.info(f"Successfully fetched {len(proxy_list)} proxies. Starting scrape...")

    jobs = scrape_jobs(
        **search_params,
        proxies=proxy_list,
        is_tls=True,
        verbose=2
    )

    if not jobs.empty:
        print(f"\nSuccessfully found {len(jobs)} jobs for Glassdoor!")
        print(jobs.head())

        # Save to CSV
        results_dir = os.path.join(project_root, "tests", "results")
        os.makedirs(results_dir, exist_ok=True)
        output_file = os.path.join(results_dir, "glassdoor_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        log.info(f"Saved results to {output_file}")
    else:
        print("\nFound no jobs for Glassdoor. The proxies may have been blocked or the search query returned no results.")