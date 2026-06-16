import streamlit as st
import pandas as pd

from streamlit_folium import st_folium

from sheets import load_sheet
from optimizer import (
    optimize_route,
    split_daily
)
from map import create_map


# Office Location
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
    min_value=10,
    value=160
)


if st.button("Generate Route"):

    try:

        # Load Sheet
        st.info("Loading sheet...")

        df = load_sheet(sheet_url)

        df.columns = df.columns.str.strip()

        st.success(
            f"Total Rows Loaded: {len(df)}"
        )

        # Validate Columns
        required_columns = [
            "Customer name",
            "Latitude",
            "Longitude",
            "1st Visit",
            "2nd Visit",
            "3rd Visit"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:

            st.error(
                f"Missing Columns: {missing}"
            )

            st.stop()

        # Filter Visit Stage
        if visit_stage == 1:

            df = df[
                df["1st Visit"]
                .astype(str)
                .str.strip()
                .str.upper()
                == "NO"
            ]

        elif visit_stage == 2:

            df = df[
                (
                    df["1st Visit"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "YES"
                )
                &
                (
                    df["2nd Visit"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "NO"
                )
            ]

        else:

            df = df[
                (
                    df["1st Visit"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "YES"
                )
                &
                (
                    df["2nd Visit"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "YES"
                )
                &
                (
                    df["3rd Visit"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == "NO"
                )
            ]

        st.success(
            f"Rows After Filter: {len(df)}"
        )

        if len(df) == 0:

            st.warning(
                "No customers found for selected visit stage."
            )

            st.stop()

        # Remove Invalid Coordinates
        df = df.dropna(
            subset=[
                "Latitude",
                "Longitude"
            ]
        )

        df["Latitude"] = pd.to_numeric(
            df["Latitude"],
            errors="coerce"
        )

        df["Longitude"] = pd.to_numeric(
            df["Longitude"],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                "Latitude",
                "Longitude"
            ]
        )

        st.success(
            f"Valid Coordinates: {len(df)}"
        )

        # Optimize Route
        st.info(
            "Optimizing route..."
        )

        route = optimize_route(
            df,
            OFFICE_LAT,
            OFFICE_LON
        )

        st.success(
            f"Optimized Stops: {len(route)}"
        )

        # Split Into Daily Routes
        days = split_daily(
            route,
            daily_limit
        )

        st.success(
            f"Days Required: {len(days)}"
        )

        # Show Daily Tables
        for day_no, day in enumerate(
            days,
            start=1
        ):

            st.subheader(
                f"Day {day_no}"
            )

            day_df = pd.DataFrame(day)

            columns_to_show = [
                c for c in [
                    "Customer name",
                    "Town",
                    "Latitude",
                    "Longitude"
                ]
                if c in day_df.columns
            ]

            st.dataframe(
                day_df[
                    columns_to_show
                ],
                use_container_width=True
            )

        # Create Map
        st.info(
            "Creating map..."
        )

        m = create_map(days)

        st_folium(
            m,
            width=1400,
            height=700
        )

        st.success(
            "Route generated successfully."
        )

    except Exception as e:

        import traceback

        st.error(
            f"ERROR:\n{str(e)}"
        )

        st.code(
            traceback.format_exc()
        )
