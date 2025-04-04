# Contains logic to calculate a privacy score and return tips. 
# Input: data from `github_check` and `hibp_check`  Output: score, grade, suggestions.

# Function definitions (just signatures + docstrings)

MAX_SCORE = 100


def calculate_score(data: dict) -> tuple[int, list[str]]:
    """
    Calculates the total privacy score and returns a list of improvement tips.
    :param data: Dictionary containing social + breach info.
    :return: (score: int, tips: list of strings)
    """

    pass