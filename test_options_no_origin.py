import requests

try:
    print("Testing OPTIONS without Origin header...")
    response = requests.options("http://127.0.0.1:8000/login")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Error: {e}")
