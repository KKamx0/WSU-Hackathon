from flask import Flask, render_template, request, jsonify
from hibp_check import check_email_breach, analyze_phone_leak  # Ensure phone_number_found is used within analyze_phone_leak

app = Flask(__name__)

class Scoring:
    def __init__(self):
        self.namePenalty = 0
        self.emailPenalty = 0
        self.birthdayPenalty = 0
        self.breachPenalty = 0
        self.locationPenalty = 0
        self.breaches = 0


    def calculate_facebook_score(self, name, email, birthday, location, friends, breaches):
        """
        Calculates a privacy score based on provided Facebook user data.
        The score starts at 100 and deductions are made for various risks:
         - Public email domains
        - Name or birthday components appearing in the email address
        - Data breaches detected for the email
        - Publicly shared location information
        Additionally, if the friend count is high, a tip is added.
        """
        score = 100
        namePenalty = 0
        emailPenalty = 0
        birthdayPenalty = 0
        breachsPenalty = 0
        locationPenalty = 0
        breaches = 0
        tips = ['Personal Tips From Your Score: ']  # Initialize tips list

        # Parse name and birthday components
        first_name = name.split()[0] if name else ""
        last_name = name.split()[1] if name and len(name.split()) > 1 else ""
        if birthday:
            birthday_parts = birthday.split('/')
            month = birthday_parts[0] if len(birthday_parts) > 0 else ""
            day = birthday_parts[1] if len(birthday_parts) > 1 else ""
            year = birthday_parts[2] if len(birthday_parts) > 2 else ""
        else:
            month = day = year = ""

        # Rule 1: Penalize for common public email domains.
        if email and any(domain in email for domain in ["gmail.com", "yahoo.com", "hotmail.com"]):
            emailPenalty = 20
            score -= emailPenalty
            tips.append("Consider using a more private email service.")

        # Rule 2: Penalize if the first or last name appears in the email.
        if first_name and first_name.lower() in email.lower():
     
            namePenalty += 10
            tips.append("Avoid using your real first name in your email address.")
        if last_name and last_name.lower() in email.lower():

            namePenalty += 10
            tips.append("Avoid using your real last name in your email address.")

        score -= namePenalty

        # Rule 3: Penalize if birthday components are in the email.
        if birthday and ((month and month in email) or (day and day in email) or (year and year in email)):
        
            birthdayPenalty += 10
            score -= birthdayPenalty
            tips.append("Avoid using your birthday in your email address.")

        # Rule 4: Penalize based on data breaches.
        if breaches:
            deduction = len(breaches) * 10
            breachsPenalty += deduction
            score -= breachsPenalty
            tips.append("Your email was found in a data breach. Change your password on those services.")
        else:
            tips.append("Your email was not found in any known breaches — great job!")

        # Rule 5: Penalize for public location.
        if location and location.lower() != "not provided":
            locationPenalty += 10
            score -= locationPenalty
            tips.append("Consider not sharing your location publicly.")

        # Additional feedback for a high friend count.
        if friends > 50:
            tips.append("Be cautious about sharing personal information with many friends.")

        # Add general privacy tips.
        tips += [
            "",
            "General Tips:",
            "Change your Facebook password regularly.",
            "Review app permissions and remove unnecessary ones.",
            "Limit post visibility to 'Friends' or custom groups.",
            "Use two-factor authentication for added protection."
        ]

        # Ensure the score doesn't go negative.
        return max(0, score), tips


