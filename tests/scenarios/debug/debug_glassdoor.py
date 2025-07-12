import os
import sys
import json
import logging
from jobspy.glassdoor import Glassdoor
from jobspy.model import ScraperInput, JobType, DescriptionFormat
from jobspy.util import create_session

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger()

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
    proxy_list = None

# Create a Glassdoor scraper instance
scraper = Glassdoor(proxies=proxy_list)

# Create scraper input
from jobspy.model import Site, Country
scraper_input = ScraperInput(
    site_type=[Site.GLASSDOOR],
    search_term="Software Engineer",
    location="Miami, FL",
    results_wanted=5,
    country=Country.USA,
    is_tls=True,
    description_format=DescriptionFormat.MARKDOWN
)

# Initialize the scraper
scraper.scraper_input = scraper_input
scraper.base_url = scraper_input.country.get_glassdoor_url()
scraper.session = create_session(
    proxies=scraper.proxies,
    ca_cert=scraper.ca_cert,
    has_retry=True,
    is_tls=scraper_input.is_tls,
)

# Get CSRF token
print("Getting CSRF token...")
token = scraper._get_csrf_token()
print(f"CSRF token: {token}")

# Update headers
from jobspy.glassdoor.constant import headers, fallback_token
headers["gd-csrf-token"] = token if token else fallback_token
scraper.session.headers.update(headers)

# Get location
print("Getting location...")
location_id, location_type = scraper._get_location(scraper_input.location, scraper_input.is_remote)
print(f"Location ID: {location_id}, Type: {location_type}")

if location_type is None:
    print("Location parsing failed")
    exit(1)

# Test the payload creation and API call
print("Creating payload...")
payload = scraper._add_payload(location_id, location_type, 1, None)
print(f"Payload created: {len(payload)} characters")

print("Making API request...")
try:
    response = scraper.session.post(
        f"{scraper.base_url}/graph",
        timeout_seconds=15,
        data=payload,
    )
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("Response content preview:")
        content = response.text[:1000]
        print(content)
        
        try:
            res_json_list = response.json()
            print(f"Response JSON type: {type(res_json_list)}")
            print(f"Response JSON length: {len(res_json_list) if isinstance(res_json_list, (list, tuple)) else 'N/A'}")
            
            if isinstance(res_json_list, (list, tuple)) and len(res_json_list) > 0:
                print(f"First element type: {type(res_json_list[0])}")
                print(f"First element keys: {list(res_json_list[0].keys()) if isinstance(res_json_list[0], dict) else 'N/A'}")
            else:
                print("Empty response or unexpected format")
                print(f"Full response: {res_json_list}")
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Request failed: {e}")
    import traceback
    traceback.print_exc() 

"""
What the Debug Script Does:
Tests each step individually:
Proxy connection
CSRF token retrieval
Location lookup
API payload creation
Raw API response inspection
Provides detailed logging:
Shows exactly what's being sent to the API
Displays response headers and content
Reveals the structure of returned data
Helps diagnose issues like:
Proxy connection problems
API response format changes
Authentication token issues
Location parsing failures
"""