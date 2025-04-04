# Main Flask app file  handles routing, user input, and rendering templates.
# This is where everything connects: form submission, API checks, scoring, and results page.

from flask import Flask, render_template, request, jsonify 

app = Flask(__name__)

# Home Page – Landing with a button or form
@app.route('/')
def landingPage():
    return render_template('index.html')  # A template with a button or form, "Click here to view your facebook privacy score"

# Route to receive form submission and show privacy score
@app.route('/fbScore', methods=['POST']) # Tips/What to do to increase personal privacy
def fbScore():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Simulated scoring logic
    score = 100  # You can plug in real logic later
    tips = [
        "Change your Facebook password regularly.",
        "Review app permissions.",
        "Limit who can see your posts.",
    ]
    
    # Send score and tips back to frontend
    return jsonify({
        'name': name,
        'email': email,
        'score': score,
        'tips': tips
    })

if __name__ == '__main__':
    app.run(debug=True)