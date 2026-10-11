"""
Tests for the rescue candidate scoring and ranking algorithm.
"""

from candidate_scoring import (
    calculate_candidate_score,
    rank_candidates
)


def test_perfect_water_rescue_candidate():
    """A candidate matching every Water Rescue preference should score 100."""

    animal = {
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 52
    }

    score = calculate_candidate_score(animal, "Water Rescue")

    assert score == 100


def test_partial_candidate_score():
    """A candidate matching breed and age but not sex should score 80."""

    animal = {
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": 52
    }

    score = calculate_candidate_score(animal, "Water Rescue")

    assert score == 80


def test_nonmatching_candidate_score():
    """A candidate matching none of the preferences should score zero."""

    animal = {
        "breed": "Poodle",
        "sex_upon_outcome": "Neutered Male",
        "age_upon_outcome_in_weeks": 200
    }

    score = calculate_candidate_score(animal, "Water Rescue")

    assert score == 0


def test_invalid_age_does_not_crash_scoring():
    """Invalid age data should be ignored instead of causing an error."""

    animal = {
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": "Unknown"
    }

    score = calculate_candidate_score(animal, "Water Rescue")

    assert score == 70


def test_unknown_rescue_type_returns_zero():
    """An unknown rescue category should return a score of zero."""

    animal = {
        "breed": "Labrador Retriever Mix",
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": 52
    }

    score = calculate_candidate_score(animal, "Unknown Rescue Type")

    assert score == 0


def test_candidates_are_ranked_highest_to_lowest():
    """Candidates should be returned in descending score order."""

    animals = [
        {
            "name": "Low Score",
            "breed": "Poodle",
            "sex_upon_outcome": "Neutered Male",
            "age_upon_outcome_in_weeks": 200
        },
        {
            "name": "Perfect Match",
            "breed": "Labrador Retriever Mix",
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": 52
        },
        {
            "name": "Partial Match",
            "breed": "Labrador Retriever Mix",
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": 52
        }
    ]

    ranked = rank_candidates(animals, "Water Rescue")

    assert ranked[0]["name"] == "Perfect Match"
    assert ranked[0]["suitability_score"] == 100

    assert ranked[1]["name"] == "Partial Match"
    assert ranked[1]["suitability_score"] == 80

    # Candidates with no matching characteristics are excluded.
    assert len(ranked) == 2


def test_ranking_does_not_modify_original_records():
    """Ranking should not add scores to the original animal records."""

    animals = [
        {
            "name": "Test Animal",
            "breed": "Labrador Retriever Mix",
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": 52
        }
    ]

    rank_candidates(animals, "Water Rescue")

    assert "suitability_score" not in animals[0]