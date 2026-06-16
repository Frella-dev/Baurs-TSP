import math


def haversine(lat1, lon1, lat2, lon2):

    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(math.radians(lat1))
        *
        math.cos(math.radians(lat2))
        *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


def optimize_route(df, office_lat, office_lon):

    remaining = []

    for _, row in df.iterrows():

        try:

            remaining.append({
                **row.to_dict(),
                "Latitude": float(row["Latitude"]),
                "Longitude": float(row["Longitude"])
            })

        except:
            pass

    route = []

    current_lat = office_lat
    current_lon = office_lon

    while remaining:

        nearest = min(
            remaining,
            key=lambda x: haversine(
                current_lat,
                current_lon,
                x["Latitude"],
                x["Longitude"]
            )
        )

        route.append(nearest)

        current_lat = nearest["Latitude"]
        current_lon = nearest["Longitude"]

        remaining.remove(nearest)

    return route


def split_daily(route, daily_km=160):

    days = []

    current_day = []

    distance_today = 0

    previous = None

    for stop in route:

        if previous:

            dist = haversine(
                previous["Latitude"],
                previous["Longitude"],
                stop["Latitude"],
                stop["Longitude"]
            )

        else:

            dist = 0

        if distance_today + dist > daily_km and len(current_day) > 0:

            days.append(current_day)

            current_day = []
            distance_today = 0

        current_day.append(stop)

        distance_today += dist

        previous = stop

    if current_day:

        days.append(current_day)

    return days
