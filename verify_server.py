
import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000"

def generate_random_email():
    return f"{''.join(random.choices(string.ascii_lowercase, k=10))}@example.com"

def test_server():
    try:
        # 1. Check Root
        print("Checking root endpoint...")
        resp = requests.get(f"{BASE_URL}/")
        if resp.status_code == 200:
            print("Server is UP.")
        else:
            print(f"Server returned {resp.status_code}")
            return

        # 2. Test Signup with Valid Email
        email = generate_random_email()
        password = "securepassword"
        print(f"Testing signup with valid email: {email}")
        resp = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})
        if resp.status_code == 200:
             print("Signup Successful.")
        else:
             print(f"Signup Failed: {resp.text}")

        # 3. Test Signup with Invalid Email
        print("Testing signup with INVALID email: 'string'")
        resp = requests.post(f"{BASE_URL}/signup", json={"email": "string", "password": password})
        if resp.status_code == 422:
             print("Invalid Email Rejected (Expected).")
        else:
             print(f"Unexpected response for invalid email: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_server()
