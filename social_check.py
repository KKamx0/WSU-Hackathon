# Handles the logic to fetch public GitHub profile data via GitHub API.
# Input: GitHub username Output: public email, location, etc.
# type: ignore
  # from Flask package
from flask import Flask, render_template, request, redirect  # type: ignore 
import requests  #  separate HTTP client library

app = Flask(__name__)

# Define the SocialCheck class
class SocialCheck:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = 'http://localhost:5000/callback'

    def get_auth_url(self):
        return (
            f"https://www.facebook.com/v12.0/dialog/oauth?"
            f"client_id={self.app_id}&redirect_uri={self.redirect_uri}&scope=email,public_profile"
        )

    def get_access_token(self, code):
        token_url = (
            f"https://graph.facebook.com/v12.0/oauth/access_token?"
            f"client_id={self.app_id}&redirect_uri={self.redirect_uri}"
            f"&client_secret={self.app_secret}&code={code}"
        )
        response = requests.get(token_url)
        return response.json().get('access_token')

    def get_user_data(self, access_token):
        user_data_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
        response = requests.get(user_data_url)
        return response.json()

# Replace with your actual app credentials
APP_ID = '4241036002877127'  # Replace with your Facebook App ID
APP_SECRET = '037ca72eb25dd1c8c73fb7465826fe6a'  # Replace with your Facebook App Secret

# Initialize the SocialCheck class
social_check = SocialCheck(APP_ID, APP_SECRET)

# Route for the landing page (button or form)
@app.route('/')
def landingPage():
    return render_template('index.html')  # Add your HTML form to submit username for privacy score

# Route for the Facebook login
@app.route('/login')
def login():
    return redirect(social_check.get_auth_url())  # Redirect to Facebook login

# Route to handle Facebook's callback with the code
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "No code provided"

    access_token = social_check.get_access_token(code)
    if not access_token:
        return "Failed to get access token"

    user_data = social_check.get_user_data(access_token)
    return f"<h2>Facebook User Data:</h2><pre>{user_data}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
