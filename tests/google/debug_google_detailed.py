import os
import re
import json
import requests
from jobspy.google.constant import headers_initial
from jobspy.util import create_session

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

# Test query
query = "software engineer jobs near San Francisco, CA"
params = {"q": query, "udm": "8"}
url = "https://www.google.com/search"

print(f"Testing query: {query}")
print(f"URL: {url}")
print(f"Params: {params}")

# Make request
response = session.get(url, headers=headers_initial, params=params)

print(f"Response status: {response.status_code}")
print(f"Response URL: {response.url}")

# Look for the cursor pattern
pattern_fc = r'<div jsname="Yust4d"[^>]+data-async-fc="([^"]+)"'
match_fc = re.search(pattern_fc, response.text)

if match_fc:
    print(f"✅ Found cursor: {match_fc.group(1)}")
else:
    print("❌ Cursor pattern not found")
    
    # Try alternative patterns
    patterns = [
        r'data-async-fc="([^"]+)"',
        r'jsname="Yust4d"[^>]*data-async-fc="([^"]+)"',
        r'<div[^>]*data-async-fc="([^"]+)"',
        r'async-fc="([^"]+)"',
    ]
    
    for i, pattern in enumerate(patterns, 1):
        match = re.search(pattern, response.text)
        if match:
            print(f"✅ Alternative pattern {i} found cursor: {match.group(1)}")
            break
        else:
            print(f"❌ Alternative pattern {i} failed: {pattern}")

# Look for job-related content
job_patterns = [
    r'520084652',
    r'jsname="Yust4d"',
    r'job-listing',
    r'data-async-fc',
    r'google\.com/search\?',
]

print("\n=== Content Analysis ===")
for pattern in job_patterns:
    matches = re.findall(pattern, response.text)
    print(f"Pattern '{pattern}': {len(matches)} matches")

# Check if the response looks like a normal Google search page
if "google.com" in response.text and "search" in response.text:
    print("✅ Response appears to be a Google search page")
else:
    print("❌ Response doesn't appear to be a Google search page")

# Save first 5000 characters of response for inspection
with open("google_response_debug.html", "w", encoding="utf-8") as f:
    f.write(response.text[:5000])
    print(f"💾 Saved first 5000 characters to google_response_debug.html")

# Check if we're getting blocked
if "blocked" in response.text.lower() or "unusual traffic" in response.text.lower():
    print("⚠️  Possible blocking detected")
    
if response.status_code == 429:
    print("⚠️  Rate limiting detected (429)")
    
if "captcha" in response.text.lower():
    print("⚠️  CAPTCHA detected")

print(f"\nResponse length: {len(response.text)} characters")
print(f"Response headers: {dict(response.headers)}") 