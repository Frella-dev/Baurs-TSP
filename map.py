import folium


def create_map(route_df):

    center_lat = route_df.iloc[0]["Latitude"]
    center_lon = route_df.iloc[0]["Longitude"]

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8
    )

    coords = []

    for i, row in route_df.iterrows():

        lat = row["Latitude"]
        lon = row["Longitude"]

        coords.append([lat, lon])

        folium.Marker(
            [lat, lon],
            popup=f"{i+1}. {row['Customer name']}"
        ).add_to(m)

    folium.PolyLine(
        coords,
        weight=5
    ).add_to(m)

    return m