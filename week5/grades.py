"""Turn a numeric score into a letter grade."""

MIN_SCORE = 0
MAX_SCORE = 100

# Lowest score for each letter, best first. Anything below the last one is an F.
GRADE_THRESHOLDS = (
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
)
FAILING_GRADE = "F"


def letter_grade(score):
    """Return the letter for a score from 0 to 100.

    Raise ValueError for a score outside that range.
    """
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError(f"score must be {MIN_SCORE}-{MAX_SCORE}, got {score}")
    for lowest, letter in GRADE_THRESHOLDS:
        if score >= lowest:
            return letter
    return FAILING_GRADE
