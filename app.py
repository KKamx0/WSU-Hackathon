# This is the main backend file (app.py) of our privacy-checking web app built with Flask.
# Main Flask app file handles: Web routing, Receiving Facebook user data (name/email) via JSON, Generating a privacy score, and Returning feedback (privacy tips) as a JSON response
from hibp_check import check_email_breach 

from flask import Flask, render_template, request, jsonify # Import necessary modules from Flask
import scoring # Import the scoring module for privacy score calculations
# Flask: creates the web app
# render_template: loads HTML pages
# request: reads incoming data (like JSON from frontend)
# jsonify: sends structured JSON data back to the frontend

# Initialize the Flask application.
app = Flask(__name__) 

# Sets up the home page route (/)
@app.route('/')
def landingPage():
    # Renders an HTML template with a form or Facebook login button
    return render_template('landing.html') 

scoring_instance = scoring.Scoring()

@app.route('/scoreBreakdown', methods=['POST'])
def scoring_breakdown():
    data = request.get_json()  # Assume data contains name, email, etc.
    name = data.get('name')
    email = data.get('email')
    birthday = data.get('birthday')
    location = data.get('location')
    friends = data.get('friends', 0)
    breaches = 0

    breaches = check_email_breach(email)

    # Use the Scoring class to calculate the score and get tips
    score, tips = scoring_instance.calculate_facebook_score(name, email, birthday, location, friends, breaches)

    # Return the result
    return render_template('scoreBreakdown.html', score=score, tips=tips)



@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/fbScore', methods=['POST'])
def fbScore():
    data = request.get_json()
    print('Received data:', data)  # Debugging line to check incoming data

    # Extract data from the request
    name = data.get('name')
    email = data.get('email')
    location = data.get('location')
    birthday = data.get('birthday')
    friends = data.get('friends', 0)  # Default to 0 if not provided
    breaches = 0

    # Check for data breaches using an external module
    breaches = check_email_breach(email)

    # Call the calculate_facebook_score function
    score, tips = scoring_instance.calculate_facebook_score(name, email, birthday, location, friends, breaches)

    # Return the response as JSON
    return jsonify({
        'name': name,
        'score': score,
        'breaches': breaches,
        'tips': tips
    })

# Starts the Flask server in debug mode so changes show immediately and errors are logged
if __name__ == '__main__':
        app.run(debug=True)
      # Run the Flask app in debug mode
    
