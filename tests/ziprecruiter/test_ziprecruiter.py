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
        "site_name": ["zip_recruiter"],
        "search_term": "Project Manager",
        "location": "Chicago, IL",
        "results_wanted": 20,
    }

    # Construct proxy string from environment variables for iproyal residential proxies
    proxy_user = os.getenv("IPROYAL_USER") or os.getenv("PROXY_USER")
    proxy_pass = os.getenv("IPROYAL_PASS") or os.getenv("PROXY_PASS")

    proxy_list = []
    if proxy_user and proxy_pass:
        # iproyal residential proxy endpoints
        iproyal_endpoints = [
            f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32101",
            f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32102",
            f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32103",
            f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32104",
            f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32105",
        ]
        proxy_list.extend(iproyal_endpoints)
        log.info(f"Using iproyal residential proxies with {len(proxy_list)} endpoints")
    else:
        log.info("No iproyal credentials found. Set IPROYAL_USER and IPROYAL_PASS environment variables.")
    
    log.info(f"Starting scrape for ZipRecruiter...")

    jobs = scrape_jobs(
        **search_params,
        proxies=proxy_list,
        verbose=2
    )

    if not jobs.empty:
        print(f"\nSuccessfully found {len(jobs)} jobs for ZipRecruiter!")
        print(jobs.head())

        # Save to CSV
        results_dir = os.path.join(project_root, "tests", "results")
        os.makedirs(results_dir, exist_ok=True)
        output_file = os.path.join(results_dir, "ziprecruiter_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        log.info(f"Saved results to {output_file}")
    else:
        print("\nFound no jobs for ZipRecruiter. The iproyal proxies may have been blocked or the search query returned no results.")