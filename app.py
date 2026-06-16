
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


if "days" not in st.session_state:
    st.session_state.days = None

if "generated" not in st.session_state:
    st.session_state.generated = False


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

        st.info("Loading Sheet...")

        df = load_sheet(sheet_url)

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

        route = optimize_route(
            df,
            OFFICE_LAT,
            OFFICE_LON
        )

        days = split_daily(
            route,
            daily_limit
        )

        st.session_state.days = days
        st.session_state.generated = True

        st.success(
            f"{len(days)} day(s) generated"
        )

    except Exception as e:

        import traceback

        st.error(str(e))

        st.code(
            traceback.format_exc()
        )


if st.session_state.generated:

    days = st.session_state.days

    st.success(
        f"Days Required: {len(days)}"
    )

    for day_no, day in enumerate(days, start=1):

        st.subheader(
            f"Day {day_no}"
        )

        day_df = pd.DataFrame(day)

        cols = [
            c for c in [
                "Customer name",
                "Town",
                "Latitude",
                "Longitude"
            ]
            if c in day_df.columns
        ]

        st.dataframe(
            day_df[cols],
            use_container_width=True
        )

        show_map = st.checkbox(
            f"Show Map Day {day_no}",
            key=f"map_checkbox_{day_no}"
        )

        if show_map:

            day_map = create_day_map(
                day,
                OFFICE_LAT,
                OFFICE_LON
            )

            st_folium(
                day_map,
                width=1200,
                height=700,
                key=f"folium_day_{day_no}"
            )

