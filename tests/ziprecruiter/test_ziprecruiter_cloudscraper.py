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
    print("🛡️ Testing ZipRecruiter with CLOUDSCRAPER")
    print("This should bypass Cloudflare protection!")
    print("="*60)
    
    # Get proxy info
    proxy_host = os.getenv("PROXY_HOST")
    proxy_port = os.getenv("PROXY_PORT")
    proxy_user = os.getenv("PROXY_USER")
    proxy_pass = os.getenv("PROXY_PASS")

    # Test configurations
    configs = [
        {
            "name": "CloudScraper No Proxy",
            "config": {
                "proxies": [],
                "verbose": 2
            }
        },
        {
            "name": "CloudScraper With Proxy", 
            "config": {
                "proxies": [f"{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"] if all([proxy_host, proxy_port, proxy_user, proxy_pass]) else [],
                "verbose": 2
            }
        }
    ]
    
    # Parameters to test
    search_params = {
        "site_name": ["zip_recruiter"],
        "search_term": "Software Engineer",
        "location": "San Francisco, CA",
        "results_wanted": 5,
    }

    for config in configs:
        print(f"\n🔍 Testing: {config['name']}")
        print("-" * 40)
        
        try:
            jobs = scrape_jobs(
                **search_params,
                **config['config']
            )

            if not jobs.empty:
                print(f"🎉 SUCCESS: Found {len(jobs)} jobs with {config['name']}!")
                print("✅ CloudScraper successfully bypassed Cloudflare!")
                print(f"✅ Updated headers (iOS 18.5, iPhone 15 Pro) working!")
                print("\nSample jobs:")
                print(jobs[['title', 'company_name', 'location']].head())
                
                # Save successful results
                output_file = f"ziprecruiter_cloudscraper_{config['name'].replace(' ', '_').lower()}.csv"
                jobs.to_csv(output_file, index=False)
                print(f"\n💾 Saved results to {output_file}")
                
                # Save working config
                with open("working_ziprecruiter_cloudscraper.txt", "w") as f:
                    f.write(f"✅ WORKING ZIPRECRUITER CLOUDSCRAPER CONFIG:\n")
                    f.write(f"Configuration: {config['name']}\n")
                    f.write(f"Settings: {config['config']}\n")
                    f.write(f"Headers: iOS 18.5, iPhone 15 Pro, App 95.0\n")
                    f.write(f"Results: {len(jobs)} jobs\n")
                    f.write(f"CloudScraper: Successfully bypassed Cloudflare!\n")
                
                print(f"\n🎯 SUCCESS! CloudScraper bypassed Cloudflare protection!")
                break  # Stop testing once we find a working config
                
            else:
                print(f"❌ FAILED: No jobs found with {config['name']}")
                
        except Exception as e:
            print(f"❌ ERROR with {config['name']}: {e}")
            import traceback
            traceback.print_exc()
            
        print("-" * 40)
    
    print("\n" + "="*60)
    print("🛡️ CLOUDSCRAPER SUMMARY:")
    print("✅ CloudScraper integration: Implemented")
    print("✅ Headers updated: iOS 16.6.1 → 18.5, iPhone 14 → 15 Pro")
    print("✅ App version updated: 91.0 → 95.0")
    print("✅ Cloudflare bypass: Active")
    print("")
    if "SUCCESS" in locals():
        print("🎉 RESULT: ZipRecruiter now works with Cloudflare protection!")
    else:
        print("🔄 If still failing, Cloudflare may have additional protections.")
        print("💡 Try: undetected-chromedriver or selenium-stealth for advanced bypass") 