# Contains logic to calculate a privacy score and return tips. 
# Input: data from `github_check` and `hibp_check`  Output: score, grade, suggestions.

# Function definitions (just signatures + docstrings)

# Simulate privacy score calculation
score = 100
tips = []

# Rule 1: public email domains
# Rule 2: name in email
# Rule 3: birthday in email
# Rule 4: data breaches
# Final tips

# Deductions and rewards based on privacy risks
POINTS = {
    'email_leak': 20,
    'password_leak': 30,
    'phone_leak': 15,
    'location_leak': 30,
    'public_profile': 5,
    'two_factor_auth': 10,
    'strong_password': 15,
    'birthdate_leak': 10,
    'public_repos': 5,
    'photo_leak': 20,
    'video_leak': 20,
    'work_leak': 20,
    'education_leak': 10,
    'pages_groups_leak': 5,  

}
# Keywords for hobbies and interests
def load_hobby_keywords(filepath: str = "hobbies.txt") -> list[str]:
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            return [line.strip().lower() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return []
    
HOBBIES = load_hobby_keywords()

# Function to calculate the score based on breach data
def score_from_breach(data: dict) -> tuple[int, int, list[str]]:
    """
    Calculates total_points score from breach data.
    Also returns the number of breach-related keywords found.
    """
    total_points = 0
    tips = []
    breach_count = 0

    # Check for breaches and calculate deductions
    if data.get('email_leak'):
        total_points -= POINTS['email_leak']
        tips.append("Consider using a different email for sensitive accounts.")
        breach_count -= POINTS['email_leak']

    if data.get('password_leak'):
        total_points -= POINTS['password_leak']
        tips.append("Change your password immediately.")
        breach_count -= POINTS['password_leak']

    if data.get('phone_leak'):
        total_points -= POINTS['phone_leak']
        tips.append("Be cautious about sharing your phone number.")
        breach_count -= POINTS['phone_leak']

    if data.get('location_leak'):
        total_points -= POINTS['location_leak']
        tips.append("Avoid sharing your location publicly.")
        breach_count -= POINTS['location_leak']

    if data.get('birthdate_leak'):
        total_points -= POINTS['birthdate_leak']
        tips.append("Be cautious about sharing your birthdate.")
        breach_count -= POINTS['birthdate_leak']

    if data.get('two_factor_auth'):
        total_points += POINTS['two_factor_auth']
        tips.append("Enable two-factor authentication for added security.")
        breach_count -= POINTS['two_factor_auth']
    
    # Social media analysis
    if data.get("exists", False):
        if not data.get("is_private", True):
            total_points -= POINTS["public_profile"]
            tips.append("Consider setting your profile to private.")
        if data.get("has_bio", False):
            total_points -= POINTS["public_bio"]
            bio_text = data.get("bio_text", "")
            breach_count -= score_from_breach(bio_text)
            tips.append("Remove personal interests from thi social media bio if unnecessary.")
        if isinstance(data.get("followers", ""), str) and "K" in data["followers"]:
            total_points -= POINTS["socialmedia_followers"]

            tips.append("Be cautious about the number of followers you have on this social media.")


    return total_points, breach_count, tips


def calculate_score(data: dict) -> tuple[int, list[str]]:
    """
    Calculates the total privacy score and returns a list of improvement tips.
    :param data: Dictionary containing social + breach info.
    :return: (score: int, tips: list of strings)
    """

def calculate_facebook_score(name, email, birthday, breaches):
    score = 100
    tips = ['Personal Tips List: ']

    first_name = name.split()[0] if name else None
    last_name = name.split()[1] if name and len(name.split()) > 1 else None

    month = birthday.split('/')[0] if birthday else None
    day = birthday.split('/')[1] if birthday else None
    year = birthday.split('/')[2] if birthday else None

    if email and any(domain in email for domain in ["gmail.com", "yahoo.com", "hotmail.com"]):
        score -= 20
        tips.append("Consider using a more private email service.")

    if first_name and first_name.lower() in email.lower():
        score -= 10
        tips.append("Avoid using your real first name in your email address.")
    if last_name and last_name.lower() in email.lower():
        score -= 10
        tips.append("Avoid using your real last name in your email address.")
    if (month in email or day in email or year in email):
        score -= 10
        tips.append("Avoid using your birthday in your email address.")

    if breaches:
        score -= len(breaches) * 10
        tips.append("Your email was found in a data breach. Change your password on those services.")
    else:
        tips.append("Your email was not found in any known breaches — great job!")

    tips += [
        ' ',
        'General Tips: ',
        "Change your Facebook password regularly.",
        "Review app permissions and remove unnecessary ones.",
        "Limit post visibility to 'Friends' or custom groups.",
        "Use two-factor authentication for added protection."
    ]

    score = max(0, score)
    return score, tips

def calculate_combined_score(fb_data, breach_data):
    fb_score, fb_tips = calculate_facebook_score(**fb_data)
    breach_score, _, breach_tips = score_from_breach(breach_data)
    
    total = max(0, fb_score + breach_score - 100)  # base score already starts at 100 in fb_score
    tips = fb_tips + breach_tips

    return total, tips
