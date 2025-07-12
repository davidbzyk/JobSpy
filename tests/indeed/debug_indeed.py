#!/usr/bin/env python3

"""
Indeed Scraper Debug Script
- Tests mobile user agents with iOS TLS fingerprinting
- Supports proxy configuration for IP blocking issues
- Includes detailed logging for debugging 403 errors
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


def test_indeed_basic():
    """Test Indeed scraping without proxies"""
    print("🔍 Testing Indeed (basic - no proxies)")
    print("=" * 50)
    
    # Use Indeed-specific search syntax
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term='"software engineer" python OR java -marketing -sales',
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
        print("\n❌ No jobs found - likely blocked by Indeed")
        print("Try using proxies or waiting for IP block to expire")


def test_indeed_with_proxies():
    """Test Indeed scraping with proxy configuration"""
    print("\n🔍 Testing Indeed (with proxies)")
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
        site_name=["indeed"],
        search_term='"python developer" django OR flask -marketing -sales',
        location="New York, NY",
        results_wanted=10,
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
        output_file = os.path.join(results_dir, "indeed_jobs.csv")
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"\n💾 Results saved to {output_file}")
    else:
        print("\n❌ No jobs found with proxy - proxy may be blocked")


def test_indeed_headers():
    """Test Indeed with specific debugging for headers"""
    print("\n🔍 Testing Indeed (header debugging)")
    print("=" * 50)
    
    print("Current Indeed configuration:")
    print("  • CloudScraper: Enabled (for Cloudflare bypass)")
    print("  • User-Agent: iPhone iOS 18.5 (mobile)")
    print("  • API Headers: iOS app simulation")
    print("  • API Endpoint: apis.indeed.com/graphql")
    
    # Test with minimal parameters to isolate issues
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term='"software engineer" -marketing -sales',
        location="CA",
        results_wanted=5,
        verbose=2
    )
    
    if not jobs.empty:
        print(f"\n✅ Headers working! Found {len(jobs)} jobs")
    else:
        print("\n❌ Headers not working - likely IP block or detection")


def test_indeed_search_syntax():
    """Test Indeed with proper search syntax"""
    print("\n🔍 Testing Indeed (proper search syntax)")
    print("=" * 50)
    
    # Test different Indeed search patterns
    search_patterns = [
        '"software engineer" python OR java -marketing -sales',
        '"data scientist" machine learning OR AI -marketing',
        '"product manager" tech OR software -insurance -sales',
        '"engineering intern" software summer 2025 -tax -marketing',
        '"frontend developer" react OR vue OR angular -marketing'
    ]
    
    for pattern in search_patterns:
        print(f"\n🔍 Testing pattern: {pattern}")
        
        jobs = scrape_jobs(
            site_name=["indeed"],
            search_term=pattern,
            location="CA",
            results_wanted=5,
            verbose=1
        )
        
        if not jobs.empty:
            print(f"  ✅ Found {len(jobs)} jobs")
            print(f"  Sample: {jobs.iloc[0]['title']} at {jobs.iloc[0]['company']}")
        else:
            print(f"  ❌ No jobs found")


def test_indeed_parameter_conflicts():
    """Test Indeed parameter limitations"""
    print("\n🔍 Testing Indeed (parameter conflicts)")
    print("=" * 50)
    
    print("⚠️  Indeed Parameter Limitations:")
    print("Only ONE of these can be used at a time:")
    print("  • hours_old")
    print("  • job_type & is_remote")
    print("  • easy_apply")
    
    # Test 1: hours_old only
    print("\n1️⃣ Testing with hours_old only...")
    jobs1 = scrape_jobs(
        site_name=["indeed"],
        search_term='"software engineer" -marketing',
        location="CA",
        hours_old=24,
        results_wanted=5,
        verbose=1
    )
    print(f"   Hours_old: {'✅' if not jobs1.empty else '❌'} {len(jobs1)} jobs")
    
    # Test 2: job_type & is_remote only
    print("\n2️⃣ Testing with job_type & is_remote only...")
    jobs2 = scrape_jobs(
        site_name=["indeed"],
        search_term='"software engineer" -marketing',
        location="CA",
        job_type="fulltime",
        is_remote=True,
        results_wanted=5,
        verbose=1
    )
    print(f"   Job_type+Remote: {'✅' if not jobs2.empty else '❌'} {len(jobs2)} jobs")
    
    # Test 3: easy_apply only
    print("\n3️⃣ Testing with easy_apply only...")
    jobs3 = scrape_jobs(
        site_name=["indeed"],
        search_term='"software engineer" -marketing',
        location="CA",
        easy_apply=True,
        results_wanted=5,
        verbose=1
    )
    print(f"   Easy_apply: {'✅' if not jobs3.empty else '❌'} {len(jobs3)} jobs")


if __name__ == "__main__":
    print("🔧 Indeed Scraper Debug Suite")
    print("=" * 50)
    
    # Test basic functionality first
    test_indeed_basic()
    
    # Test with proxies if available
    test_indeed_with_proxies()
    
    # Test header configuration
    test_indeed_headers()
    
    # Test Indeed-specific search syntax
    test_indeed_search_syntax()
    
    # Test parameter limitations
    test_indeed_parameter_conflicts()
    
    print("\n📝 Indeed Debugging Tips:")
    print("  • Indeed uses CloudScraper to bypass Cloudflare protection")
    print("  • Mobile app API with iOS headers for authenticity")
    print("  • 403 errors usually indicate Cloudflare blocking or IP issues")
    print("  • Use residential proxies for best results")
    print("  • Wait 1-2 hours if getting consistent 403 errors")
    print("  • CloudScraper automatically handles Cloudflare challenges")
    print("\n🔍 Indeed Search Syntax:")
    print('  • Use quotes for exact match: "software engineer"')
    print("  • Use OR for alternatives: python OR java")
    print("  • Use - to exclude: -marketing -sales")
    print('  • Example: "engineering intern" software summer 2025 -tax -marketing')
    print("\n⚠️  Indeed Parameter Limitations:")
    print("  • Only ONE of these can be used at a time:")
    print("    - hours_old")
    print("    - job_type & is_remote")
    print("    - easy_apply")
    print("  • Indeed searches job descriptions too (causes unrelated results)")
    print("  • Use proper filtering to get relevant jobs") 