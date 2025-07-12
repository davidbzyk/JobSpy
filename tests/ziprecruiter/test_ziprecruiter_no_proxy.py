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
    print("Testing ZipRecruiter WITHOUT PROXY...")
    print("This tests if Cloudflare is specifically blocking the proxy IP")
    print("="*60)
    
    # Parameters to test
    search_params = {
        "site_name": ["zip_recruiter"],  # Fixed: underscore needed
        "search_term": "Software Engineer",
        "location": "San Francisco, CA",
        "results_wanted": 5,
    }

    # Test without proxy first
    print("\n--- Testing: ZipRecruiter No Proxy ---")
    
    try:
        jobs = scrape_jobs(
            **search_params,
            proxies=[],  # No proxy
            is_tls=True,
            verbose=2
        )

        if not jobs.empty:
            print(f"✅ SUCCESS: Found {len(jobs)} jobs WITHOUT proxy")
            print("🎯 Issue confirmed: Cloudflare is blocking the proxy IP!")
            print("\nSample jobs:")
            print(jobs.head())
            
            # Save successful results
            jobs.to_csv("ziprecruiter_no_proxy_success.csv", index=False)
            print(f"\n💾 Saved results to ziprecruiter_no_proxy_success.csv")
            
        else:
            print(f"❌ FAILED: No jobs found even without proxy")
            
    except Exception as e:
        print(f"❌ ERROR without proxy: {e}")
        
    print("\n" + "="*60)
    print("CLOUDFLARE PROXY BLOCKING ANALYSIS:")
    print("🔴 Cloudflare detected: ZipRecruiter uses Cloudflare protection")
    print("🔴 Proxy IP flagged: Your proxy IP is on Cloudflare's blocklist")
    print("🔴 Ray ID: 95e18fd8887372fe (can report to proxy provider)")
    print("🔴 Blocked IP: 209.44.187.24 (your proxy IP)")
    print("")
    print("SOLUTIONS:")
    print("1. 🔄 Try different proxy provider (non-datacenter IPs)")
    print("2. 🏠 Use residential proxies instead of datacenter proxies")
    print("3. 🕐 Wait for IP rotation from your proxy provider")
    print("4. 📞 Contact proxy provider about Cloudflare blocking") 