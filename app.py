import streamlit as st
import pandas as pd

from sheets import load_sheet
from optimizer import optimize_route, split_daily

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

        st.info("Loading Google Sheet")

        df = load_sheet(sheet_url)

        st.write(
            "Rows Loaded:",
            len(df)
        )

        df.columns = df.columns.str.strip()

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

        st.write(
            "Rows After Filter:",
            len(df)
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

        st.write(
            "Valid Coordinates:",
            len(df)
        )

        route = optimize_route(
            df,
            OFFICE_LAT,
            OFFICE_LON
        )

        st.write(
            "Optimized Stops:",
            len(route)
        )

        days = split_daily(
            route,
            daily_limit
        )

        st.success(
            f"Days Required: {len(days)}"
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

        st.success(
            "Route Generated Successfully"
        )

    except Exception as e:

        import traceback

        st.error(str(e))

        st.code(
            traceback.format_exc()
        )
