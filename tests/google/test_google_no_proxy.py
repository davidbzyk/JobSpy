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
    print("Testing Google WITHOUT proxy...")
    
    # Try different search terms that might work better
    test_queries = [
        "product manager jobs in United States",
        "software engineer jobs near San Francisco CA",
        "data scientist jobs",
        "marketing manager jobs",
        "python developer jobs"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Testing: {query}")
        print('='*50)
        
        try:
            jobs = scrape_jobs(
                site_name=["google"],
                google_search_term=query,
                results_wanted=5,
                proxies=[],  # NO PROXY
                is_tls=True,
                verbose=2
            )
            
            if not jobs.empty:
                print(f"✅ SUCCESS: Found {len(jobs)} jobs")
                print(jobs.head())
                
                # Save successful results
                output_file = f"google_success_{query.replace(' ', '_')}.csv"
                jobs.to_csv(output_file, index=False)
                print(f"💾 Saved to {output_file}")
                
                # Save working config
                with open("working_google_config.txt", "w") as f:
                    f.write(f"WORKING GOOGLE CONFIG:\n")
                    f.write(f"Query: {query}\n")
                    f.write(f"Proxy: None\n")
                    f.write(f"TLS: True\n")
                    f.write(f"Results: {len(jobs)} jobs\n")
                
                print("🎉 SUCCESS! Check working_google_config.txt for details")
                break  # Stop testing once we find a working query
                
            else:
                print("❌ FAILED: No jobs found")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
    print("\n" + "="*50)
    print("Test complete. If any query worked, the config was saved.") 