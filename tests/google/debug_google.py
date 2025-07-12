#!/usr/bin/env python3

"""
Google Jobs Scraper Debug Script
- Tests desktop user agent strategy
- Supports proxy configuration
- Includes Google-specific search term handling
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


def test_google_basic():
    """Test Google Jobs scraping without proxies"""
    print("🔍 Testing Google Jobs (basic - no proxies)")
    print("=" * 50)
    
    jobs = scrape_jobs(
        site_name=["google"],
        google_search_term="software engineer jobs in San Francisco, CA",
        results_wanted=10,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ SUCCESS! Found {len(jobs)} jobs")
        print("\nSample jobs:")
        for i, job in jobs.head(3).iterrows():
            print(f"  • {job['title']} at {job['company']}")
    else:
        print("\n❌ No jobs found - check google_search_term format")
        print("Google requires very specific search syntax")


def test_google_with_proxies():
    """Test Google Jobs scraping with proxy configuration"""
    print("\n🔍 Testing Google Jobs (with proxies)")
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
        site_name=["google"],
        google_search_term="product manager jobs in New York, NY since yesterday",
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
        output_file = os.path.join(results_dir, "google_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"\n💾 Results saved to {output_file}")
    else:
        print("\n❌ No jobs found with proxy - check search term format")


def test_google_search_terms():
    """Test Google Jobs with different search term formats"""
    print("\n🔍 Testing Google Jobs (search term formats)")
    print("=" * 50)
    
    search_terms = [
        "python developer jobs in San Francisco",
        "remote software engineer jobs",
        "data scientist jobs near me",
        "marketing manager jobs since last week",
        "entry level developer jobs in California"
    ]
    
    for search_term in search_terms:
        print(f"\n🔍 Testing: '{search_term}'")
        
        jobs = scrape_jobs(
            site_name=["google"],
            google_search_term=search_term,
            results_wanted=5,
            verbose=1
        )
        
        if not jobs.empty:
            print(f"  ✅ Found {len(jobs)} jobs")
        else:
            print(f"  ❌ No jobs found")


def test_google_headers():
    """Test Google Jobs header configuration"""
    print("\n🔍 Testing Google Jobs (headers)")
    print("=" * 50)
    
    print("Current Google Jobs configuration:")
    print("  • User-Agent: Chrome on macOS (desktop)")
    print("  • Headers: Chrome browser headers")
    print("  • Search: Uses google_search_term parameter")
    print("  • Location: Embedded in search term")
    
    # Test with minimal parameters
    jobs = scrape_jobs(
        site_name=["google"],
        google_search_term="engineer jobs",
        results_wanted=5,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ Headers working! Found {len(jobs)} jobs")
    else:
        print("\n❌ Headers not working or search term too generic")


def test_google_time_filters():
    """Test Google Jobs with time-based filters"""
    print("\n🔍 Testing Google Jobs (time filters)")
    print("=" * 50)
    
    time_filters = [
        "software engineer jobs posted today",
        "data analyst jobs since yesterday",
        "product manager jobs posted this week",
        "developer jobs posted last month"
    ]
    
    for filter_term in time_filters:
        print(f"\n⏰ Testing: '{filter_term}'")
        
        jobs = scrape_jobs(
            site_name=["google"],
            google_search_term=filter_term,
            results_wanted=5,
            verbose=1
        )
        
        if not jobs.empty:
            print(f"  ✅ Found {len(jobs)} jobs with time filter")
        else:
            print(f"  ❌ No jobs found with time filter")


if __name__ == "__main__":
    print("🔧 Google Jobs Scraper Debug Suite")
    print("=" * 50)
    
    # Test basic functionality first
    test_google_basic()
    
    # Test with proxies if available
    test_google_with_proxies()
    
    # Test different search terms
    test_google_search_terms()
    
    # Test headers
    test_google_headers()
    
    # Test time filters
    test_google_time_filters()
    
    print("\n📝 Google Jobs Debugging Tips:")
    print("  • Google Jobs uses google_search_term parameter (not search_term)")
    print("  • Search terms must be very specific and natural language")
    print("  • Desktop user agent is used (Chrome on macOS)")
    print("  • Include location in the search term: 'jobs in San Francisco'")
    print("  • Time filters work: 'since yesterday', 'posted today', etc.")
    print("  • Google is generally less restrictive than other job boards")
    print("  • Copy search terms directly from Google Jobs website for best results") 