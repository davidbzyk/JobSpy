import os
import traceback
from jobspy import scrape_jobs

print("Testing the successful Google configuration:")
print("Query: product manager jobs in United States")
print("Config: TLS=True, No Proxy")
print("="*50)

try:
    jobs = scrape_jobs(
        site_name=["google"],
        google_search_term="product manager jobs in United States",
        results_wanted=5,
        is_tls=True,
        proxies=[],  # No proxy
        verbose=2    # Full debugging
    )
    
    if not jobs.empty:
        print(f"✅ SUCCESS: Found {len(jobs)} jobs")
        
        # Let's examine the data structure safely
        print("\n=== Job Data Structure ===")
        for i, job in jobs.iterrows():
            print(f"\nJob {i+1}:")
            print(f"  ID: {job.get('id', 'N/A')}")
            print(f"  Title: {job.get('title', 'N/A')}")
            print(f"  Company: {job.get('company_name', 'N/A')}")
            print(f"  Location: {job.get('location', 'N/A')}")
            print(f"  URL: {job.get('job_url', 'N/A')}")
            print(f"  Date: {job.get('date_posted', 'N/A')}")
            
        # Save the successful results
        output_file = "successful_google_jobs.csv"
        jobs.to_csv(output_file, index=False)
        print(f"\n💾 Saved {len(jobs)} jobs to {output_file}")
        
        # Show the successful configuration
        print("\n=== WORKING CONFIGURATION ===")
        print("site_name: ['google']")
        print("google_search_term: 'product manager jobs in United States'")
        print("is_tls: True")
        print("proxies: []  # No proxy")
        print("="*50)
        
    else:
        print("❌ FAILED: No jobs found")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\n=== Full Error Traceback ===")
    traceback.print_exc()
    print("="*50) 