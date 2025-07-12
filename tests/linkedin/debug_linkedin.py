#!/usr/bin/env python3

"""
LinkedIn Scraper Debug Script
- Tests desktop user agent strategy
- Supports proxy configuration for rate limiting
- Includes detailed logging for debugging blocks
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


def test_linkedin_basic():
    """Test LinkedIn scraping without proxies"""
    print("🔍 Testing LinkedIn (basic - no proxies)")
    print("=" * 50)
    
    jobs = scrape_jobs(
        site_name=["linkedin"],
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
        print("\n❌ No jobs found - likely rate limited by LinkedIn")
        print("LinkedIn is very aggressive with rate limiting")


def test_linkedin_with_proxies():
    """Test LinkedIn scraping with proxy configuration"""
    print("\n🔍 Testing LinkedIn (with proxies)")
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
        site_name=["linkedin"],
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
        output_file = os.path.join(results_dir, "linkedin_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"\n💾 Results saved to {output_file}")
    else:
        print("\n❌ No jobs found with proxy - may be rate limited")


def test_linkedin_with_description():
    """Test LinkedIn with full description fetching"""
    print("\n🔍 Testing LinkedIn (with full descriptions)")
    print("=" * 50)
    
    print("⚠️  This test fetches full job descriptions (slower)")
    
    jobs = scrape_jobs(
        site_name=["linkedin"],
        search_term="data scientist",
        location="San Francisco, CA",
        results_wanted=5,
        linkedin_fetch_description=True,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ SUCCESS! Found {len(jobs)} jobs with descriptions")
        print("\nSample job with description:")
        job = jobs.iloc[0]
        print(f"  • {job['title']} at {job['company']}")
        print(f"  • Description length: {len(job['description']) if job['description'] else 0} chars")
    else:
        print("\n❌ No jobs found with descriptions")


def test_linkedin_rate_limiting():
    """Test LinkedIn rate limiting behavior"""
    print("\n🔍 Testing LinkedIn (rate limiting behavior)")
    print("=" * 50)
    
    print("Current LinkedIn configuration:")
    print("  • User-Agent: Chrome on macOS (desktop)")
    print("  • Rate Limiting: Very aggressive (usually around page 10)")
    print("  • Delay: 3 seconds between requests")
    print("  • Band Delay: 4 seconds additional")
    
    # Test with small batches
    for batch in range(3):
        print(f"\n📦 Testing batch {batch + 1}...")
        
        jobs = scrape_jobs(
            site_name=["linkedin"],
            search_term="engineer",
            location="CA",
            results_wanted=5,
            offset=batch * 5,
            verbose=1
        )
        
        if not jobs.empty:
            print(f"  ✅ Batch {batch + 1}: Found {len(jobs)} jobs")
        else:
            print(f"  ❌ Batch {batch + 1}: No jobs found - likely rate limited")
            break


if __name__ == "__main__":
    print("🔧 LinkedIn Scraper Debug Suite")
    print("=" * 50)
    
    # Test basic functionality first
    test_linkedin_basic()
    
    # Test with proxies if available
    test_linkedin_with_proxies()
    
    # Test with full descriptions
    test_linkedin_with_description()
    
    # Test rate limiting behavior
    test_linkedin_rate_limiting()
    
    print("\n📝 LinkedIn Debugging Tips:")
    print("  • LinkedIn is the most restrictive job board")
    print("  • Rate limiting usually kicks in around page 10")
    print("  • Desktop user agent is used (Chrome on macOS)")
    print("  • Proxies are essential for large-scale scraping")
    print("  • linkedin_fetch_description=True gets full job details (slower)")
    print("  • Use smaller batch sizes to avoid rate limiting")
    print("  • Consider using linkedin_company_ids for targeted scraping") 