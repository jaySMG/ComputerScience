"""
Visualization functions for the Grazioso Salvare Rescue Animal Dashboard.

Keeping chart creation separate from the dashboard callbacks makes the
visualization code easier to maintain and reuse.
"""

import pandas as pd
import dash_leaflet as dl
import plotly.express as px
from dash import html


def create_breed_chart(data=None, breed_counts=None):
    """Create a pie chart using MongoDB breed counts when available."""

    try:
        # Prefer summarized breed counts produced by MongoDB aggregation.
        if breed_counts:
            breed_data = pd.DataFrame(breed_counts)

            if (
                not breed_data.empty
                and "breed" in breed_data.columns
                and "count" in breed_data.columns
            ):
                return px.pie(
                    breed_data,
                    names="breed",
                    values="count",
                    title="Breeds Represented in Current Results"
                )

        # Fall back to the existing DataFrame-based behavior.
        if data is None or data.empty or "breed" not in data.columns:
            return px.pie(
                title="No Breed Data Available"
            )

        breed_data = data.dropna(subset=["breed"])

        if breed_data.empty:
            return px.pie(
                title="No Breed Data Available"
            )

        return px.pie(
            breed_data,
            names="breed",
            title="Breeds Represented in Current Results"
        )

    except (KeyError, ValueError, TypeError) as error:
        print(f"Unable to create breed chart: {error}")

        return px.pie(
            title="Unable to Display Breed Chart"
        )

def create_animal_map(data, row):
    """Create a map showing the location of the selected animal."""

    # Make sure the requested row exists.
    if data.empty or row < 0 or row >= len(data):
        return html.Div("No animal location is available.")

    animal = data.iloc[row]

    # Make sure location information exists before creating the map.
    latitude = animal.get("location_lat")
    longitude = animal.get("location_long")

    if pd.isna(latitude) or pd.isna(longitude):
        return html.Div(
            "Location information is not available for this animal.",
            style={"textAlign": "center", "padding": "20px"}
        )

    try:
        latitude = float(latitude)
        longitude = float(longitude)

        return dl.Map(
            style={
                "width": "100%",
                "height": "500px"
            },
            center=[latitude, longitude],
            zoom=10,
            children=[
                dl.TileLayer(id="base-layer-id"),

                dl.Marker(
                    position=[latitude, longitude],
                    children=[
                        dl.Tooltip(str(animal.get("breed", "Unknown Breed"))),

                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(str(animal.get("name", "Unknown")))
                        ])
                    ]
                )
            ]
        )

    except (TypeError, ValueError):
        return html.Div(
            "The location information for this animal is invalid.",
            style={"textAlign": "center", "padding": "20px"}
        )