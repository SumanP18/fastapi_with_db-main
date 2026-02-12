
from utils.ai_response import generate_image
import requests

try:
    print("Testing generate_image utility...")
    url = generate_image("a beautiful sunset")
    print("Generated URL:", url)
    
    print("\nVerifying URL is accessible...")
    r = requests.get(url, timeout=10)
    print("Status Code:", r.status_code)
    if r.status_code == 200:
        print("SUCCESS: Image generation logic and service are working.")
    else:
        print("FAILED: Service returned", r.status_code)
except Exception as e:
    print("ERROR:", e)
