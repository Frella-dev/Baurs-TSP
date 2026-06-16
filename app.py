import streamlit as st
import pandas as pd

from streamlit_folium import st_folium

from sheets import load_sheet
from optimizer import (
    optimize_route,
    split_daily
)
from map import create_map


OFFICE_LAT = 6.8275814230546725
OFFICE_LON = 79.95698659415302


st.set_page_config(
    page_title="Sales Route Planner",
    layout="wide"
)

st.title("Sales Route Planner")

sheet_url = st.text_input(
    "Google Sheet URL"
)

visit_stage = st.selectbox(
    "Visit Stage",
    [1, 2, 3]
)

daily_limit = st.number_input(
    "Daily KM Limit",
    value=160
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

    st.success(
        f"{len(df)} customers found"
    )

    route = optimize_route(
        df,
        OFFICE_LAT,
        OFFICE_LON
    )

    days = split_daily(
        route,
        daily_limit
    )

    st.success(
        f"{len(days)} days required"
    )

    for day_no, day in enumerate(days, start=1):

        st.subheader(
            f"Day {day_no}"
        )

        day_df = pd.DataFrame(day)

        st.dataframe(
            day_df[
                [
                    "Customer name",
                    "Town",
                    "Latitude",
                    "Longitude"
                ]
            ],
            use_container_width=True
        )

    m = create_map(days)

    st_folium(
        m,
        width=1400,
        height=700
    )
