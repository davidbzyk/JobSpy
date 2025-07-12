import os
import re
from jobspy import scrape_jobs

# Get proxy from environment
proxy_host = os.getenv("PROXY_HOST")
proxy_port = os.getenv("PROXY_PORT")
proxy_user = os.getenv("PROXY_USER")
proxy_pass = os.getenv("PROXY_PASS")

if all([proxy_host, proxy_port, proxy_user, proxy_pass]):
    proxy = f"{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    proxy_list = [proxy]
    print(f"Using proxy: {proxy_host}:{proxy_port}")
else:
    print("No proxy configured")
    proxy_list = []

# Test configurations
test_configs = [
    {
        "name": "TLS=False, With Proxy",
        "config": {
            "is_tls": False,
            "proxies": proxy_list,
            "verbose": 1
        }
    },
    {
        "name": "TLS=False, No Proxy",
        "config": {
            "is_tls": False,
            "proxies": [],
            "verbose": 1
        }
    },
    {
        "name": "TLS=True, No Proxy",
        "config": {
            "is_tls": True,
            "proxies": [],
            "verbose": 1
        }
    },
    {
        "name": "TLS=True, With Proxy (Original)",
        "config": {
            "is_tls": True,
            "proxies": proxy_list,
            "verbose": 1
        }
    },
]

# Test search terms that worked before
test_queries = [
    "software engineer jobs near San Francisco, CA since yesterday",
    "product manager jobs in United States",
    "software engineer jobs"
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Testing Query: {query}")
    print('='*60)
    
    for config in test_configs:
        print(f"\n--- {config['name']} ---")
        
        try:
            jobs = scrape_jobs(
                site_name=["google"],
                google_search_term=query,
                results_wanted=5,
                **config['config']
            )
            
            if not jobs.empty:
                print(f"✅ SUCCESS: Found {len(jobs)} jobs")
                print(f"Sample job: {jobs.iloc[0]['title']} at {jobs.iloc[0]['company_name']}")
                
                # This worked! Save the config
                with open("working_google_config.txt", "w") as f:
                    f.write(f"WORKING CONFIG:\n")
                    f.write(f"Query: {query}\n")
                    f.write(f"Config: {config}\n")
                    f.write(f"Jobs found: {len(jobs)}\n")
                print("💾 Saved working config to working_google_config.txt")
                
                # Don't test other configs for this query since we found one that works
                break
            else:
                print("❌ FAILED: No jobs found")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
        print("-" * 30)
    
    print("\n" + "="*60)

print("\n=== Test Complete ===")
print("If any configuration worked, check working_google_config.txt for details.") 