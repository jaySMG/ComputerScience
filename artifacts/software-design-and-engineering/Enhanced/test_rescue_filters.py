"""
Tests for the Grazioso Salvare rescue filtering logic.

These tests verify that each dashboard rescue option produces
the expected MongoDB query without requiring a database connection.
"""

from rescue_filters import get_rescue_query


def test_water_rescue_query():
    """Verify the Water Rescue filter."""

    query = get_rescue_query("Water Rescue")

    assert query["animal_type"] == "Dog"
    assert query["sex_upon_outcome"] == "Intact Female"
    assert "Labrador Retriever Mix" in query["breed"]["$in"]
    assert query["age_upon_outcome_in_weeks"]["$gte"] == 26
    assert query["age_upon_outcome_in_weeks"]["$lte"] == 156


def test_mountain_rescue_query():
    """Verify the Mountain or Wilderness Rescue filter."""

    query = get_rescue_query("Mountain or Wilderness Rescue")

    assert query["animal_type"] == "Dog"
    assert query["sex_upon_outcome"] == "Intact Male"
    assert "German Shepherd" in query["breed"]["$in"]
    assert query["age_upon_outcome_in_weeks"]["$gte"] == 26
    assert query["age_upon_outcome_in_weeks"]["$lte"] == 156


def test_disaster_tracking_query():
    """Verify the Disaster or Individual Tracking filter."""

    query = get_rescue_query("Disaster or Individual Tracking")

    assert query["animal_type"] == "Dog"
    assert query["sex_upon_outcome"] == "Intact Male"
    assert "Bloodhound" in query["breed"]["$in"]
    assert query["age_upon_outcome_in_weeks"]["$gte"] == 20
    assert query["age_upon_outcome_in_weeks"]["$lte"] == 300


def test_reset_query():
    """Verify that Reset returns an unrestricted query."""

    query = get_rescue_query("Reset")

    assert query == {}


def test_unknown_filter_returns_all_records():
    """Verify that an unknown filter safely falls back to all records."""

    query = get_rescue_query("Unknown Rescue Type")

    assert query == {}