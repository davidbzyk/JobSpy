#!/usr/bin/env python3

"""
Example: Using iproyal residential proxies with JobSpy
"""

import os
from jobspy import scrape_jobs

def main():
    # Set up your iproyal residential proxy credentials
    # Option 1: Set environment variables (recommended for security)
    # export IPROYAL_USER="your_username"
    # export IPROYAL_PASS="your_password"
    
    # Option 2: Use hardcoded credentials (update with your details)
    iproyal_user = os.getenv("IPROYAL_USER") or "your_username"
    iproyal_pass = os.getenv("IPROYAL_PASS") or "your_password"
    
    # iproyal residential proxy endpoints
    # These endpoints automatically rotate through different residential IPs
    iproyal_proxies = [
        f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32101",
        f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32102",
        f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32103",
        f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32104",
        f"{iproyal_user}:{iproyal_pass}@rotating-residential.iproyal.com:32105",
    ]
    
    print("🔍 Scraping ZipRecruiter with iproyal residential proxies...")
    print(f"Using {len(iproyal_proxies)} iproyal endpoints")
    
    # Scrape jobs using iproyal residential proxies
    jobs = scrape_jobs(
        site_name=["zip_recruiter"],
        search_term="software engineer",
        location="New York, NY",
        results_wanted=20,
        proxies=iproyal_proxies,
        verbose=2,  # Enable debug logging to see proxy rotation
    )
    
    if not jobs.empty:
        print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
        print("\n📊 Sample jobs:")
        for i, job in jobs.head(5).iterrows():
            print(f"  {i+1}. {job['title']} at {job['company']}")
            print(f"     Location: {job['location']}")
            print(f"     URL: {job['job_url']}")
            print()
        
        # Save results
        jobs.to_csv("ziprecruiter_jobs.csv", index=False)
        print(f"💾 Results saved to ziprecruiter_jobs.csv")
        
    else:
        print("❌ No jobs found. Check your:")
        print("  • iproyal credentials")
        print("  • Network connection")
        print("  • Search parameters")

if __name__ == "__main__":
    main() 