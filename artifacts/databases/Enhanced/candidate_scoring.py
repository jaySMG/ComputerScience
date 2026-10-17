"""
Rescue Candidate Scoring

This module scores animal records based on how closely they match
the preferred characteristics for a selected rescue category.
"""


RESCUE_PROFILES = {
    "Water Rescue": {
        "breeds": [
            "Labrador Retriever Mix",
            "Chesapeake Bay Retriever Mix",
            "Newfoundland Mix"
        ],
        "sex": "Intact Female",
        "min_age": 26,
        "max_age": 156
    },

    "Mountain or Wilderness Rescue": {
        "breeds": [
            "German Shepherd",
            "Alaskan Malamute",
            "Old English Sheepdog",
            "Siberian Husky",
            "Rottweiler"
        ],
        "sex": "Intact Male",
        "min_age": 26,
        "max_age": 156
    },

    "Disaster or Individual Tracking": {
        "breeds": [
            "Doberman Pinscher",
            "German Shepherd",
            "Golden Retriever",
            "Bloodhound",
            "Rottweiler"
        ],
        "sex": "Intact Male",
        "min_age": 20,
        "max_age": 300
    }
}


WEIGHTS = {
    "breed": 50,
    "age": 30,
    "sex": 20
}


def calculate_candidate_score(animal, rescue_type):
    """
    Calculate a suitability score for one animal.

    The score is based on breed, age, and sex. A perfect match
    receives 100 points.
    """

    profile = RESCUE_PROFILES.get(rescue_type)

    if profile is None:
        return 0

    score = 0

    # Breed has the highest weight because breed characteristics
    # are important when selecting animals for specialized work.
    if animal.get("breed") in profile["breeds"]:
        score += WEIGHTS["breed"]

    # Award points when the animal is within the preferred age range.
    age = animal.get("age_upon_outcome_in_weeks")

    if age is not None:
        try:
            age = float(age)

            if profile["min_age"] <= age <= profile["max_age"]:
                score += WEIGHTS["age"]

        except (TypeError, ValueError):
            pass

    # Award points when the animal matches the preferred sex.
    if animal.get("sex_upon_outcome") == profile["sex"]:
        score += WEIGHTS["sex"]

    return score


def rank_candidates(animals, rescue_type):
    """
    Score and rank animal records from highest to lowest suitability.

    A copy of each record is created so the original data is not
    modified.
    """

    ranked_candidates = []

    for animal in animals:
        candidate = animal.copy()

        candidate["suitability_score"] = calculate_candidate_score(
            candidate,
            rescue_type
        )

        ranked_candidates.append(candidate)

    # Remove animals that do not match any rescue criteria.
    ranked_candidates = [
        candidate
        for candidate in ranked_candidates
        if candidate["suitability_score"] > 0
    ]

    # Rank the remaining candidates from highest to lowest score.
    ranked_candidates.sort(
        key=lambda candidate: candidate["suitability_score"],
        reverse=True
    )

    return ranked_candidates