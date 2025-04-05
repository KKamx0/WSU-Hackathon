# Handles HaveIBeenPwned email breach checking (mock or real).
# Input: email → Output: list of breached services.
# Check if the user’s email from Facebook has been leaked, and return a list of services like Dropbox, LinkedIn, etc. where it was leaked.

# Show them the breached services 
# Recommend privacy tips like changing passwords, enabling 2FA, etc.

# Imports the requests library to make HTTP API calls:
import requests
import re

# Function that detects phone numbers in bio text
def phone_number_found(text: str) -> bool:
# Checks if the input text contains a phone number-like pattern.
# The regex pattern matches various formats of phone numbers, including optional country codes and separators.
    pattern = r'(\+?\d{1,2})?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}'
    return bool(re.search(pattern, text))

# Function that handles phone leak analysis
def analyze_phone_leak(user_data: dict, tips: list, total_score: int) -> int:

    # Example usage inside your privacy scoring logic:
    if phone_number_found(user_data.get("bio_text", "")):
        tips.append("Avoid posting your phone number in public bios.")
        total_score -= 15  # Default to 15 if not defined

    # Example of using the HIBP API to check for breaches related to a phone number.
    api_key = 'your_api_key'
    headers = {'hibp-api-key': api_key, 'user-agent': 'PrivacyAnalyzer'}
    phone = '1234567890'  # Not guaranteed to work, based on breach availability

    res = requests.get(
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{phone}",
    headers=headers
    )

    if res.status_code == 200:
        print("Phone number found in breach")
    else:
        print("No known breaches for phone number")

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



