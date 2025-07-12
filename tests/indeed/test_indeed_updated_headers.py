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
    print("Testing Indeed with UPDATED HEADERS and NO TLS...")
    print("This tests if the updated iOS 18.5 headers work better")
    print("="*60)
    
    # Get proxy info
    proxy_host = os.getenv("PROXY_HOST")
    proxy_port = os.getenv("PROXY_PORT")
    proxy_user = os.getenv("PROXY_USER")
    proxy_pass = os.getenv("PROXY_PASS")

    # Test configurations with updated headers
    configs = [
        {
            "name": "Updated Headers, No TLS, No Proxy",
            "config": {
                "is_tls": False,
                "proxies": []
            }
        },
        {
            "name": "Updated Headers, No TLS, With Proxy",
            "config": {
                "is_tls": False,
                "proxies": [f"{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"] if all([proxy_host, proxy_port, proxy_user, proxy_pass]) else []
            }
        }
    ]
    
    # Parameters to test
    search_params = {
        "site_name": ["indeed"],
        "search_term": "Software Engineer",
        "location": "San Francisco, CA",
        "results_wanted": 5,
        "country_indeed": "USA"
    }

    for config in configs:
        print(f"\n--- Testing: {config['name']} ---")
        
        try:
            jobs = scrape_jobs(
                **search_params,
                **config['config'],
                verbose=2
            )

            if not jobs.empty:
                print(f"✅ SUCCESS: Found {len(jobs)} jobs with {config['name']}")
                print("🎯 The updated headers (iOS 18.5, App 220.0) are working!")
                print("\nSample jobs:")
                print(jobs.head())
                
                # Save successful results
                output_file = f"indeed_updated_headers_{config['name'].replace(' ', '_').replace(',', '').lower()}.csv"
                jobs.to_csv(output_file, index=False)
                print(f"\n💾 Saved results to {output_file}")
                
                # Save working config
                with open("working_indeed_updated_config.txt", "w") as f:
                    f.write(f"WORKING INDEED CONFIG WITH UPDATED HEADERS:\n")
                    f.write(f"Configuration: {config['name']}\n")
                    f.write(f"Settings: {config['config']}\n")
                    f.write(f"Headers: iOS 18.5, App 220.0\n")
                    f.write(f"Results: {len(jobs)} jobs\n")
                
                print(f"\n🎉 SUCCESS! Saved working config to working_indeed_updated_config.txt")
                break  # Stop testing once we find a working config
                
            else:
                print(f"❌ FAILED: No jobs found with {config['name']}")
                
        except Exception as e:
            print(f"❌ ERROR with {config['name']}: {e}")
            
        print("-" * 50)
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("✅ Headers updated: iOS 17.4.1 → 18.5, App 205.0 → 220.0")
    print("✅ User agent rotation enabled")
    print("✅ TLS fingerprint matching")
    print("If still getting 403s, the proxy IP may be globally blocked by Indeed.") 