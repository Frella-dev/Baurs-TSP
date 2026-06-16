import streamlit as st
import pandas as pd

from streamlit_folium import st_folium

from sheets import load_sheet
from ors import build_matrix
from optimizer import optimize_route
from map import create_map


st.set_page_config(
    page_title="Sales Route Planner",
    layout="wide"
)

st.title("Sales Route Planner")

sheet_url = st.text_input(
    "Google Sheet URL"
)

ors_key = st.text_input(
    "OpenRouteService Key",
    type="password"
)

visit_stage = st.selectbox(
    "Visit Stage",
    [1, 2, 3]
)

if st.button("Generate Route"):

    df = load_sheet(sheet_url)

    if visit_stage == 1:

        df = df[
            df["1st Visit"] == "No"
        ]

    elif visit_stage == 2:

        df = df[
            (df["1st Visit"] == "Yes")
            &
            (df["2nd Visit"] == "No")
        ]

    else:

        df = df[
            (df["1st Visit"] == "Yes")
            &
            (df["2nd Visit"] == "Yes")
            &
            (df["3rd Visit"] == "No")
        ]

    office_lat = 6.8275814230546725
    office_lon = 79.95698659415302

    locations = [
        [office_lon, office_lat]
    ]

    for _, row in df.iterrows():

        locations.append([
            row["Longitude"],
            row["Latitude"]
        ])

    matrix = build_matrix(
        locations,
        ors_key
    )

    route = optimize_route(matrix)

    rows = []

    for idx in route[1:]:

        rows.append(
            df.iloc[idx - 1]
        )

    route_df = pd.DataFrame(rows)

    st.subheader(
        "Optimized Route"
    )

    st.dataframe(
        route_df[
            [
                "Customer name",
                "Town",
                "Latitude",
                "Longitude"
            ]
        ]
    )

    m = create_map(route_df)

    st_folium(
        m,
        width=1400,
        height=700
    )