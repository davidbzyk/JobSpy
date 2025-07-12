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
    print("Testing Indeed WITHOUT proxy...")
    print("This will test if your proxy IP is being blocked by Indeed")
    print("="*60)
    
    # Parameters to test
    search_params = {
        "site_name": ["indeed"],
        "search_term": "Software Engineer",
        "location": "San Francisco, CA",
        "results_wanted": 5,
        "country_indeed": "USA"
    }

    try:
        jobs = scrape_jobs(
            **search_params,
            proxies=[],  # NO PROXY
            is_tls=True,  # Keep TLS fingerprinting
            verbose=2
        )

        if not jobs.empty:
            print(f"✅ SUCCESS WITHOUT PROXY: Found {len(jobs)} jobs")
            print("🎯 This confirms your proxy IP is being blocked by Indeed")
            print("\nSample jobs:")
            print(jobs.head())
            
            # Save results
            output_file = "indeed_no_proxy_success.csv"
            jobs.to_csv(output_file, index=False)
            print(f"\n💾 Saved results to {output_file}")
            
            print("\n" + "="*60)
            print("SOLUTION FOUND:")
            print("1. Your proxy IP is blocked by Indeed")
            print("2. Try different proxy regions/endpoints if available")
            print("3. Or rotate between multiple proxy IPs")
            print("4. Contact your proxy provider for fresh IPs")
            print("="*60)
            
        else:
            print("❌ FAILED EVEN WITHOUT PROXY")
            print("This suggests Indeed is blocking your main IP too")
            print("You may need to wait or try from a different network")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc() 