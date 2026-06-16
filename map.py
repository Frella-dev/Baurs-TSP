import folium


def create_map(days):

    if not days:
        return folium.Map(
            location=[7.5, 80.7],
            zoom_start=7
        )

    first = days[0][0]

    m = folium.Map(
        location=[
            float(first["Latitude"]),
            float(first["Longitude"])
        ],
        zoom_start=8
    )

    for day_no, day in enumerate(days, start=1):

        coords = []

        for idx, stop in enumerate(day, start=1):

            lat = float(stop["Latitude"])
            lon = float(stop["Longitude"])

            coords.append([lat, lon])

            folium.Marker(
                [lat, lon],
                popup=f"Day {day_no} - {idx}",
                tooltip=str(
                    stop.get(
                        "Customer name",
                        "Customer"
                    )
                )
            ).add_to(m)

        if len(coords) > 1:

            folium.PolyLine(
                coords,
                weight=4
            ).add_to(m)

    return m
