import requests


def build_matrix(coords, api_key):

    url = "https://api.openrouteservice.org/v2/matrix/driving-car"

    payload = {
        "locations": coords,
        "metrics": ["distance"]
    }

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=120
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    if response.status_code != 200:

        raise Exception(
            f"""
ORS ERROR

Status:
{response.status_code}

Response:
{response.text}
"""
        )

    data = response.json()

    if "distances" not in data:

        raise Exception(
            f"""
No distances returned.

Response:
{response.text}
"""
        )

    return data["distances"]
