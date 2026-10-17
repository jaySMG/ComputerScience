"""
Tests for dashboard visualization functions.
"""

import pandas as pd
import pandas as pd

from visualization import create_breed_chart, create_animal_map




def test_breed_chart_is_created():
    """Verify that breed data produces a Plotly pie chart."""

    data = pd.DataFrame([
        {"breed": "Labrador Retriever Mix"},
        {"breed": "German Shepherd"},
        {"breed": "Labrador Retriever Mix"}
    ])

    figure = create_breed_chart(data)

    assert figure is not None
    assert len(figure.data) > 0
    assert figure.data[0].type == "pie"


def test_breed_chart_uses_breed_data():
    """Verify that the breed chart contains the supplied breeds."""

    data = pd.DataFrame([
        {"breed": "Labrador Retriever Mix"},
        {"breed": "German Shepherd"}
    ])

    figure = create_breed_chart(data)

    labels = list(figure.data[0].labels)

    assert "Labrador Retriever Mix" in labels
    assert "German Shepherd" in labels


def test_animal_map_is_created():
    """Verify that valid location data produces a map."""

    data = pd.DataFrame([
        {
            "breed": "Labrador Retriever Mix",
            "name": "Test Animal",
            "location_lat": 30.75,
            "location_long": -97.48
        }
    ])

    animal_map = create_animal_map(data, 0)

    assert animal_map is not None


def test_animal_map_contains_marker():
    """Verify that the animal map contains a location marker."""

    data = pd.DataFrame([
        {
            "breed": "German Shepherd",
            "name": "Test Dog",
            "location_lat": 30.75,
            "location_long": -97.48
        }
    ])

    animal_map = create_animal_map(data, 0)

    # The map should contain a tile layer and animal marker.
    assert len(animal_map.children) == 2

    marker = animal_map.children[1]

    assert marker.position == [30.75, -97.48]