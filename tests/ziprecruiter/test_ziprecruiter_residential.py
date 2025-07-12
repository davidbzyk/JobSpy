#!/usr/bin/env python3

"""
Test script for ZipRecruiter with residential proxies
"""

import os
import sys
import logging

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from jobspy import scrape_jobs

# Configure logging to see proxy rotation in action
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_residential_proxies():
    """
    Test ZipRecruiter with iproyal residential proxies
    """
    
    # iproyal residential proxy configuration
    # Replace with your actual iproyal credentials
    iproyal_proxies = [
        "username:password@rotating-residential.iproyal.com:32101",
        "username:password@rotating-residential.iproyal.com:32102",
        "username:password@rotating-residential.iproyal.com:32103",
        "username:password@rotating-residential.iproyal.com:32104",
        "username:password@rotating-residential.iproyal.com:32105",
        # iproyal provides multiple endpoints for load balancing
        # You can add more endpoints or use environment variables
    ]
    
    # Alternative: Get from environment variables (more secure)
    iproyal_user = os.getenv("IPROYAL_USER")
    iproyal_pass = os.getenv("IPROYAL_PASS")
    
    if iproyal_user and iproyal_pass:
        # Use environment variables if available
        iproyal_proxies = [
            f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32101",
            f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32102",
            f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32103",
            f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32104",
            f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32105",
        ]
        print("Using iproyal credentials from environment variables")
    else:
        print("Using hardcoded iproyal credentials (update with your details)")
        # You'll need to update the proxies above with your actual credentials
    
    print("Testing ZipRecruiter with iproyal residential proxies...")
    print(f"Using {len(iproyal_proxies)} iproyal residential proxies")
    
    # Test parameters
    search_params = {
        "site_name": ["zip_recruiter"],
        "search_term": "software engineer",
        "location": "New York, NY",
        "results_wanted": 5,  # Small number for testing
        "verbose": 2,
        "proxies": iproyal_proxies
    }
    
    try:
        jobs = scrape_jobs(**search_params)
        
        if not jobs.empty:
            print(f"\n✅ SUCCESS! Found {len(jobs)} jobs using residential proxies")
            print("\nFirst few job titles:")
            for i, job in jobs.head(3).iterrows():
                print(f"  • {job['title']} at {job['company']}")
        else:
            print("\n❌ No jobs found. Check your proxy configuration.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("This might indicate proxy authentication issues or blocked IPs.")

def test_proxy_format():
    """
    Test different proxy formats to ensure they work
    """
    test_formats = [
        "user:pass@proxy.com:8080",
        "http://user:pass@proxy.com:8080", 
        "https://user:pass@proxy.com:8080",
        "proxy.com:8080",
    ]
    
    print("\nTesting proxy format handling...")
    for proxy_format in test_formats:
        print(f"  • {proxy_format}")
        # You can add actual format testing here if needed

if __name__ == "__main__":
    print("🔍 ZipRecruiter iproyal Residential Proxy Test")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--format-test":
        test_proxy_format()
    else:
        test_residential_proxies()
    
    print("\n📝 Tips for using iproyal residential proxies with ZipRecruiter:")
    print("  • Use format: username:password@rotating-residential.iproyal.com:32101")
    print("  • iproyal provides multiple endpoints (32101-32105) for load balancing")
    print("  • Set environment variables: IPROYAL_USER and IPROYAL_PASS")
    print("  • The scraper will automatically rotate through your proxy endpoints")
    print("  • Each page request uses a different proxy endpoint")
    print("  • Monitor the debug logs to see proxy rotation in action")
    print("  • If you get 403/429 errors, try using different country targeting in iproyal")
    print("  • iproyal rotating endpoints automatically change IP addresses") 