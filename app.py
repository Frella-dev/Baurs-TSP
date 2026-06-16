import streamlit as st
import pandas as pd

from streamlit_folium import st_folium

from sheets import load_sheet
from optimizer import optimize_route, split_daily
from map import create_day_map


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

        st.info("Loading Google Sheet...")

        df = load_sheet(sheet_url)

        st.write(
            "Total Rows Loaded:",
            len(df)
        )

        df.columns = df.columns.str.strip()

        required_columns = [
            "Customer name",
            "Latitude",
            "Longitude",
            "1st Visit",
            "2nd Visit",
            "3rd Visit"
        ]

        missing = [
            c for c in required_columns
            if c not in df.columns
        ]

        if missing:

            st.error(
                f"Missing Columns: {missing}"
            )

            st.stop()

        # -------------------------
        # Visit Stage Filter
        # -------------------------

        if visit_stage == 1:

            df = df[
                df["1st Visit"]
                .astype(str)
                .str.upper()
                .str.strip()
                == "NO"
            ]

        elif visit_stage == 2:

            df = df[
                (
                    df["1st Visit"]
                    .astype(str)
                    .str.upper()
                    .str.strip()
                    == "YES"
                )
                &
                (
                    df["2nd Visit"]
                    .astype(str)
                    .str.upper()
                    .str.strip()
                    == "NO"
                )
            ]

        else:

            df = df[
                (
                    df["1st Visit"]
                    .astype(str)
                    .str.upper()
                    .str.strip()
                    == "YES"
                )
                &
                (
                    df["2nd Visit"]
                    .astype(str)
                    .str.upper()
                    .str.strip()
                    == "YES"
                )
                &
                (
                    df["3rd Visit"]
                    .astype(str)
                    .str.upper()
                    .str.strip()
                    == "NO"
                )
            ]

        st.success(
            f"Rows After Filter: {len(df)}"
        )

        if len(df) == 0:

            st.warning(
                "No customers found."
            )

            st.stop()

        # -------------------------
        # Coordinate Cleanup
        # -------------------------

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

        # -------------------------
        # Route Optimization
        # -------------------------

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

        # -------------------------
        # Daily Split
        # -------------------------

        days = split_daily(
            route,
            daily_limit
        )

        st.success(
            f"Days Required: {len(days)}"
        )

        # -------------------------
        # Day Views
        # -------------------------

        for day_no, day in enumerate(
            days,
            start=1
        ):

            st.subheader(
                f"Day {day_no}"
            )

            day_df = pd.DataFrame(day)

            display_cols = [
                c for c in [
                    "Customer name",
                    "Town",
                    "Latitude",
                    "Longitude"
                ]
                if c in day_df.columns
            ]

            st.dataframe(
                day_df[display_cols],
                use_container_width=True
            )

            with st.expander(
                f"View Map - Day {day_no}"
            ):

                day_map = create_day_map(
                    day,
                    OFFICE_LAT,
                    OFFICE_LON
                )

                st_folium(
                    day_map,
                    width=1200,
                    height=700,
                    key=f"map_{day_no}"
                )

        st.success(
            "Route Generated Successfully"
        )

    except Exception as e:

        import traceback

        st.error(
            f"ERROR: {str(e)}"
        )

        st.code(
            traceback.format_exc()
        )
