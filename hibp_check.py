# Handles HaveIBeenPwned email breach checking (mock or real).
# Input: email → Output: list of breached services.
# Check if the user’s email from Facebook has been leaked, and return a list of services like Dropbox, LinkedIn, etc. where it was leaked.

# Show them the breached services 
# Recommend privacy tips like changing passwords, enabling 2FA, etc.

# Imports the requests library to make HTTP API calls:
import requests

# When True, it skips the real API and returns fake data.
USE_MOCK_DATA = True

def check_email_breach(email):
    # If in mock mode, it calls mock_breach_result() 
    if USE_MOCK_DATA:
        return mock_breach_result(email) 

    # If Not Mock: Sends Real API Request
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    # Requires a valid API key (you can get one at HIBP API)
    headers = {
        "hibp-api-key": "your_api_key_here",
        "user-agent": "PrivacyScoreTool"
    }
    response = requests.get(url, headers=headers) # Sends a GET request to HIBP API 


    # Interprets the API Response
    if response.status_code == 200:
        breaches = response.json()
        return [b['Name'] for b in breaches]
    elif response.status_code == 404:
        return []  # No breaches
    else:
        print(f"Error: {response.status_code}")
        return None
    
# Simulated Breach Checker
def mock_breach_result(email):
    # Simulated results for testing/demo
    if "test" in email:
        return ["Dropbox", "LinkedIn"]  # Fake breach list
    else:
        return []

# For testing
if __name__ == "__main__":
    print(check_email_breach("test@example.com")) # should return ["Dropbox", "LinkedIn"]

