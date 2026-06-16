import folium


def create_day_map(day, office_lat, office_lon):

    if len(day) == 0:
        return folium.Map(
            location=[office_lat, office_lon],
            zoom_start=8
        )

    first = day[0]

    m = folium.Map(
        location=[
            first["Latitude"],
            first["Longitude"]
        ],
        zoom_start=9
    )

    coords = []

    folium.Marker(
        [office_lat, office_lon],
        popup="Office",
        tooltip="Office"
    ).add_to(m)

    coords.append(
        [office_lat, office_lon]
    )

    for idx, stop in enumerate(day, start=1):

        lat = float(stop["Latitude"])
        lon = float(stop["Longitude"])

        coords.append([lat, lon])

        folium.Marker(
            [lat, lon],
            popup=f"{idx}. {stop['Customer name']}",
            tooltip=f"{idx}. {stop['Customer name']}"
        ).add_to(m)

    folium.PolyLine(
        coords,
        weight=5
    ).add_to(m)

    return m
