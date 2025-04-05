# This is the main backend file (app.py) of our privacy-checking web app built with Flask.
# Main Flask app file handles: Web routing, Receiving Facebook user data (name/email) via JSON, Generating a privacy score, and Returning feedback (privacy tips) as a JSON response
from hibp_check import check_email_breach 
from scoring import calculate_facebook_score
from flask import Flask, render_template, request, jsonify # Import necessary modules from Flask
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

@app.route('/scoringBreakdown')
def scoring_breakdown():
    # Extract query parameters, such as score or tips
    score = request.args.get('score')
    tips = request.args.get('tips')
    return render_template('scoringBreakdown.html', score=score)

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

    # Check for data breaches using an external module
    breaches = check_email_breach(email)

    # Call the calculate_facebook_score function
    score, tips = calculate_facebook_score(name, email, birthday, location, friends, breaches)

    # Return the response as JSON
    return jsonify({
        'name': name,
        'score': score,
        'breaches': breaches,
        'tips': tips
    })
# # Defines a new POST route /fbScore that receives data from the frontend (via fetch)
# @app.route('/fbScore', methods=['POST'])
# def fbScore():
#     data = request.get_json()
#     print('Received data:', data)  # Debugging line to check incoming data
    
#     name = data.get('name')
#     first_name = name.split()[0] if name else None
#     last_name = name.split()[1] if name and len(name.split()) > 1 else None
#     email = data.get('email')
#     location = data.get('location')
#     birthday = data.get('birthday')
#     month = birthday.split('/')[0] if birthday else None
#     day = birthday.split('/')[1] if birthday else None
#     year = birthday.split('/')[2] if birthday else None
#     friends = data.get('friends', 0)  # Default to 0 if not provided

#     # Simulate privacy score calculation
#     score = 100
#     tips = ['Personal Tips From Your Score: ']  # Initialize tips list

#     # Rule 1: Penalize for public email domains
#     if email and any(domain in email for domain in ["gmail.com", "yahoo.com", "hotmail.com"]):
#         score -= 10
#         tips.append("Consider using a more private email service.")

#     # Rule 2: Penalize for using name and birthday in email
#     if first_name and first_name.lower() in email.lower():
#         score -= 15
#         tips.append("Avoid using your real first name in your email address.")
#     if last_name and last_name.lower() in email.lower():
#         score -= 15
#         # Penalize for using last name in email
#         tips.append("Avoid using your real last name in your email address.")
    
#     if (month in email or day in email or year in email):
#         score -= 10
#         tips.append("Avoid using your birthday in your email address.")
    
#     # Rule 3: Check for data breaches via HaveIBeenPwned
#     breaches = check_email_breach(email)
#     if breaches:
#         score -= len(breaches) * 10
#         tips.append("Your email was found in a data breach. Change your password on those services.")
#     else:
#         tips.append("Your email was not found in any known breaches — great job!")

#     # Rule 4: Penalize for public location
#     if location and location.lower() != "not provided":
#         score -= 10
#         tips.append("Consider not sharing your location publicly.")

#     # Final tips (always helpful)
#     tips += [
#         ' ',
#         'General Tips: ',
#         "Change your Facebook password regularly.",
#         "Review app permissions and remove unnecessary ones.",
#         "Limit post visibility to 'Friends' or custom groups.",
#         "Use two-factor authentication for added protection."
#     ]

#     if friends>50:
#         tips.append("Be cautious about sharing personal information with many friends.")


#     score = max(0, score)  # Prevent negative score

#     return jsonify({
#         'name': name,
#         'score': score,
#         'breaches': breaches,
#         'tips': tips
#     })


# Starts the Flask server in debug mode so changes show immediately and errors are logged
if __name__ == '__main__':
        app.run(debug=False)
      # Run the Flask app in debug mode
    
