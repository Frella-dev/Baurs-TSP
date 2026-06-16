import folium


def create_map(days):

    first = days[0][0]

    m = folium.Map(
        location=[
            first["Latitude"],
            first["Longitude"]
        ],
        zoom_start=8
    )

    for day_no, day in enumerate(days, start=1):

        coords = []

        for idx, stop in enumerate(day, start=1):

            lat = stop["Latitude"]
            lon = stop["Longitude"]

            coords.append([lat, lon])

            folium.Marker(
                [lat, lon],
                popup=f"Day {day_no} - {idx}. {stop['Customer name']}"
            ).add_to(m)

        folium.PolyLine(
            coords,
            weight=4
        ).add_to(m)

    return m
