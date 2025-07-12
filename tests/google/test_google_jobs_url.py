import os
import re
import json
from jobspy.util import create_session
from jobspy.google.constant import headers_initial

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

# Create session
session = create_session(
    proxies=proxy_list,
    is_tls=True,
    has_retry=True,
)

# Test different Google Jobs URLs
test_urls = [
    # Original search with udm=8
    "https://www.google.com/search?q=software+engineer+jobs&udm=8",
    
    # Direct Google Jobs URL
    "https://www.google.com/search?q=software+engineer+jobs&ibp=htl;jobs",
    
    # Jobs filter parameter
    "https://www.google.com/search?q=jobs+software+engineer&tbs=qdr:w",
    
    # Simple jobs search
    "https://www.google.com/search?q=software+engineer+jobs",
    
    # Try without any special parameters
    "https://www.google.com/search?q=jobs",
]

for i, url in enumerate(test_urls, 1):
    print(f"\n=== Test {i}: {url} ===")
    
    try:
        response = session.get(url, headers=headers_initial)
        print(f"Status: {response.status_code}")
        
        # Check for redirect/enablejs
        if "enablejs" in response.text:
            print("❌ Got enablejs redirect - detected as bot")
        elif "jobs" in response.text.lower() and "google" in response.text.lower():
            print("✅ Got Google page with jobs content")
            
            # Look for job-related patterns
            job_indicators = [
                "data-async-fc",
                "jsname=\"Yust4d\"",
                "520084652",
                "job-listing",
                "Apply on",
                "salary",
                "company",
            ]
            
            found_indicators = []
            for indicator in job_indicators:
                if indicator.lower() in response.text.lower():
                    found_indicators.append(indicator)
            
            if found_indicators:
                print(f"✅ Found job indicators: {found_indicators}")
                
                # Look for the cursor pattern
                pattern_fc = r'data-async-fc="([^"]+)"'
                match_fc = re.search(pattern_fc, response.text)
                if match_fc:
                    print(f"✅ Found cursor: {match_fc.group(1)[:50]}...")
                else:
                    print("❌ No cursor found")
                    
                # Save this successful response
                with open(f"google_success_{i}.html", "w", encoding="utf-8") as f:
                    f.write(response.text[:10000])
                    print(f"💾 Saved to google_success_{i}.html")
            else:
                print("❌ No job indicators found")
        else:
            print("❌ Unexpected response")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("-" * 50)

print("\n=== Summary ===")
print("If any tests succeeded, check the saved HTML files for the working URL format.")
print("You may need to manually visit Google Jobs to get the correct search term format.") 