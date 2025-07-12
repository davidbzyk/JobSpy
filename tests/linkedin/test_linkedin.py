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
        "site_name": ["linkedin"],
        "search_term": "Data Analyst",
        "location": "New York, NY",
        "results_wanted": 20,
        # "linkedin_fetch_description": True, # Uncomment to get full descriptions (slower)
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
        log.warning("Could not fetch any proxies. LinkedIn may block requests.")

    log.info(f"Starting scrape for LinkedIn...")

    jobs = scrape_jobs(
        **search_params,
        proxies=proxy_list,
        # is_tls=True is highly recommended for modern sites like LinkedIn to avoid blocks
        is_tls=True,
        verbose=2
    )

    if not jobs.empty:
        print(f"\nSuccessfully found {len(jobs)} jobs for LinkedIn!")
        print(jobs.head())

        # Save to CSV
        results_dir = os.path.join(project_root, "tests", "results")
        os.makedirs(results_dir, exist_ok=True)
        output_file = os.path.join(results_dir, "linkedin_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        log.info(f"Saved results to {output_file}")
    else:
        print("\nFound no jobs for LinkedIn. The proxies may have been blocked or the search query returned no results.")