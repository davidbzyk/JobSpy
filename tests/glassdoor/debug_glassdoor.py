#!/usr/bin/env python3

"""
Glassdoor Scraper Debug Script
- Tests desktop user agent strategy
- Supports proxy configuration
- Includes GraphQL API debugging
"""

import os
import sys
import logging
import csv

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from jobspy import scrape_jobs

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger()


def test_glassdoor_basic():
    """Test Glassdoor scraping without proxies"""
    print("🔍 Testing Glassdoor (basic - no proxies)")
    print("=" * 50)
    
    jobs = scrape_jobs(
        site_name=["glassdoor"],
        search_term="software engineer",
        location="San Francisco, CA",
        results_wanted=10,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ SUCCESS! Found {len(jobs)} jobs")
        print("\nSample jobs:")
        for i, job in jobs.head(3).iterrows():
            print(f"  • {job['title']} at {job['company']}")
    else:
        print("\n❌ No jobs found - may be blocked by Glassdoor")
        print("Glassdoor uses GraphQL API with CSRF tokens")


def test_glassdoor_with_proxies():
    """Test Glassdoor scraping with proxy configuration"""
    print("\n🔍 Testing Glassdoor (with proxies)")
    print("=" * 50)
    
    # Get proxy configuration from environment
    proxy_user = os.getenv("PROXY_USER")
    proxy_pass = os.getenv("PROXY_PASS")
    proxy_host = os.getenv("PROXY_HOST")
    proxy_port = os.getenv("PROXY_PORT")
    
    proxy_list = []
    if all([proxy_user, proxy_pass, proxy_host, proxy_port]):
        proxy = f"{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        proxy_list.append(proxy)
        print(f"Using proxy: {proxy_host}:{proxy_port}")
    else:
        print("No proxy configuration found. Set environment variables:")
        print("  - PROXY_USER")
        print("  - PROXY_PASS")
        print("  - PROXY_HOST")
        print("  - PROXY_PORT")
        return
    
    jobs = scrape_jobs(
        site_name=["glassdoor"],
        search_term="product manager",
        location="New York, NY",
        results_wanted=15,
        proxies=proxy_list,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ SUCCESS! Found {len(jobs)} jobs with proxy")
        print("\nSample jobs:")
        for i, job in jobs.head(3).iterrows():
            print(f"  • {job['title']} at {job['company']}")
            
        # Save results
        results_dir = os.path.join(project_root, "tests", "results")
        os.makedirs(results_dir, exist_ok=True)
        output_file = os.path.join(results_dir, "glassdoor_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"\n💾 Results saved to {output_file}")
    else:
        print("\n❌ No jobs found with proxy - may be blocked")


def test_glassdoor_countries():
    """Test Glassdoor with different countries"""
    print("\n🔍 Testing Glassdoor (different countries)")
    print("=" * 50)
    
    countries = ["USA", "Canada", "UK"]
    
    for country in countries:
        print(f"\n🌍 Testing country: {country}")
        
        jobs = scrape_jobs(
            site_name=["glassdoor"],
            search_term="developer",
            location="Remote",
            country_indeed=country,
            results_wanted=5,
            verbose=1
        )
        
        if not jobs.empty:
            print(f"  ✅ Found {len(jobs)} jobs in {country}")
        else:
            print(f"  ❌ No jobs found in {country}")


def test_glassdoor_graphql():
    """Test Glassdoor GraphQL API behavior"""
    print("\n🔍 Testing Glassdoor (GraphQL API)")
    print("=" * 50)
    
    print("Current Glassdoor configuration:")
    print("  • API: GraphQL endpoint")
    print("  • User-Agent: Chrome on macOS (desktop)")
    print("  • CSRF Token: Automatically fetched")
    print("  • Headers: Apollo GraphQL client headers")
    
    # Test with minimal parameters
    jobs = scrape_jobs(
        site_name=["glassdoor"],
        search_term="manager",
        location="CA",
        results_wanted=5,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ GraphQL API working! Found {len(jobs)} jobs")
    else:
        print("\n❌ GraphQL API not working - check CSRF token or blocking")


def test_glassdoor_remote_jobs():
    """Test Glassdoor remote job filtering"""
    print("\n🔍 Testing Glassdoor (remote jobs)")
    print("=" * 50)
    
    jobs = scrape_jobs(
        site_name=["glassdoor"],
        search_term="software engineer",
        location="Remote",
        is_remote=True,
        results_wanted=10,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ Found {len(jobs)} remote jobs")
        print("\nSample remote jobs:")
        for i, job in jobs.head(3).iterrows():
            print(f"  • {job['title']} at {job['company']}")
            print(f"    Remote: {job.get('is_remote', 'N/A')}")
    else:
        print("\n❌ No remote jobs found")


if __name__ == "__main__":
    print("🔧 Glassdoor Scraper Debug Suite")
    print("=" * 50)
    
    # Test basic functionality first
    test_glassdoor_basic()
    
    # Test with proxies if available
    test_glassdoor_with_proxies()
    
    # Test different countries
    test_glassdoor_countries()
    
    # Test GraphQL API
    test_glassdoor_graphql()
    
    # Test remote jobs
    test_glassdoor_remote_jobs()
    
    print("\n📝 Glassdoor Debugging Tips:")
    print("  • Glassdoor uses GraphQL API with CSRF tokens")
    print("  • Desktop user agent is used (Chrome on macOS)")
    print("  • CSRF tokens are automatically fetched from job pages")
    print("  • Supports multiple countries (USA, Canada, UK, etc.)")
    print("  • Remote job filtering is available")
    print("  • Rate limiting is moderate compared to LinkedIn")
    print("  • Job descriptions are fetched in separate requests") 