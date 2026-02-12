
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def simulate_frontend_login():
    email = "newuser@example.com"
    password = "newpassword123"

    print(f"1. Creating user {email}...")
    signup_resp = requests.post(
        f"{BASE_URL}/signup", 
        json={"email": email, "password": password}
    )
    print(f"Signup Status: {signup_resp.status_code}")
    print(f"Signup Response: {signup_resp.text}")

    print(f"\n2. Attempting login with {email}...")
    # Mimic the frontend fetch structure
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'email': email,
        'password': password
    }
    
    try:
        login_resp = requests.post(
            f"{BASE_URL}/login",
            headers=headers,
            json=payload
        )
        
        print(f"Login Status: {login_resp.status_code}")
        print(f"Login Response: {login_resp.text}")
        
        if login_resp.status_code == 200:
            print("SUCCESS: Login worked with frontend-style request.")
        else:
            print("FAILURE: Login failed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simulate_frontend_login()
