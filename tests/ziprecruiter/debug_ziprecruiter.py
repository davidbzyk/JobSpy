#!/usr/bin/env python3

"""
ZipRecruiter Scraper Debug Script
- Tests CloudScraper with Cloudflare bypass
- Supports iproyal residential proxy rotation
- Includes mobile user agent simulation
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


def test_ziprecruiter_basic():
    """Test ZipRecruiter scraping without proxies"""
    print("🔍 Testing ZipRecruiter (basic - no proxies)")
    print("=" * 50)
    
    jobs = scrape_jobs(
        site_name=["zip_recruiter"],
        search_term="project manager",
        location="Chicago, IL",
        results_wanted=10,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ SUCCESS! Found {len(jobs)} jobs")
        print("\nSample jobs:")
        for i, job in jobs.head(3).iterrows():
            print(f"  • {job['title']} at {job['company']}")
    else:
        print("\n❌ No jobs found - may be blocked by Cloudflare")
        print("Try using residential proxies")


def test_ziprecruiter_with_iproyal():
    """Test ZipRecruiter scraping with iproyal residential proxies"""
    print("\n🔍 Testing ZipRecruiter (with iproyal residential proxies)")
    print("=" * 50)
    
    # Get iproyal configuration from environment
    proxy_user = os.getenv("IPROYAL_USER") or os.getenv("PROXY_USER")
    proxy_pass = os.getenv("IPROYAL_PASS") or os.getenv("PROXY_PASS")
    
    if not (proxy_user and proxy_pass):
        print("No iproyal configuration found. Set environment variables:")
        print("  - IPROYAL_USER (or PROXY_USER)")
        print("  - IPROYAL_PASS (or PROXY_PASS)")
        return
    
    # iproyal residential proxy endpoints
    iproyal_proxies = [
        f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32101",
        f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32102",
        f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32103",
        f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32104",
        f"{proxy_user}:{proxy_pass}@rotating-residential.iproyal.com:32105",
    ]
    
    print(f"Using {len(iproyal_proxies)} iproyal residential proxy endpoints")
    
    jobs = scrape_jobs(
        site_name=["zip_recruiter"],
        search_term="software engineer",
        location="New York, NY",
        results_wanted=15,
        proxies=iproyal_proxies,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ SUCCESS! Found {len(jobs)} jobs with iproyal proxies")
        print("\nSample jobs:")
        for i, job in jobs.head(3).iterrows():
            print(f"  • {job['title']} at {job['company']}")
            
        # Save results
        results_dir = os.path.join(project_root, "tests", "results")
        os.makedirs(results_dir, exist_ok=True)
        output_file = os.path.join(results_dir, "ziprecruiter_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"\n💾 Results saved to {output_file}")
    else:
        print("\n❌ No jobs found with iproyal proxies")
        print("Check your iproyal credentials and network connectivity")


def test_ziprecruiter_cloudflare():
    """Test ZipRecruiter CloudFlare bypass capability"""
    print("\n🔍 Testing ZipRecruiter (CloudFlare bypass)")
    print("=" * 50)
    
    print("Current ZipRecruiter configuration:")
    print("  • CloudScraper: Enabled (for Cloudflare bypass)")
    print("  • User-Agent: iPhone iOS 18.5 (mobile app simulation)")
    print("  • Headers: iOS app headers")
    print("  • Proxy Rotation: Enabled")
    
    # Test with minimal parameters
    jobs = scrape_jobs(
        site_name=["zip_recruiter"],
        search_term="manager",
        location="CA",
        results_wanted=5,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ CloudFlare bypass working! Found {len(jobs)} jobs")
    else:
        print("\n❌ CloudFlare bypass not working - may need residential proxies")


def test_ziprecruiter_multiple_locations():
    """Test ZipRecruiter with multiple locations"""
    print("\n🔍 Testing ZipRecruiter (multiple locations)")
    print("=" * 50)
    
    locations = ["New York, NY", "Los Angeles, CA", "Chicago, IL"]
    
    for location in locations:
        print(f"\n📍 Testing location: {location}")
        
        jobs = scrape_jobs(
            site_name=["zip_recruiter"],
            search_term="developer",
            location=location,
            results_wanted=5,
            verbose=1
        )
        
        if not jobs.empty:
            print(f"  ✅ Found {len(jobs)} jobs in {location}")
        else:
            print(f"  ❌ No jobs found in {location}")


if __name__ == "__main__":
    print("🔧 ZipRecruiter Scraper Debug Suite")
    print("=" * 50)
    
    # Test basic functionality first
    test_ziprecruiter_basic()
    
    # Test with iproyal proxies
    test_ziprecruiter_with_iproyal()
    
    # Test CloudFlare bypass
    test_ziprecruiter_cloudflare()
    
    # Test multiple locations
    test_ziprecruiter_multiple_locations()
    
    print("\n📝 ZipRecruiter Debugging Tips:")
    print("  • ZipRecruiter uses CloudScraper for Cloudflare bypass")
    print("  • Mobile user agent simulates iPhone app")
    print("  • Residential proxies (iproyal) work best")
    print("  • Proxy rotation happens on each request")
    print("  • 403/429 errors indicate rate limiting or blocking")
    print("  • CloudFlare challenges are automatically handled") 