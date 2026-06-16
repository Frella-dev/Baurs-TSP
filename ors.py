import requests

def build_matrix(coords, api_key):

    url = "https://api.openrouteservice.org/v2/matrix/driving-car"

    body = {
        "locations": coords,
        "metrics": ["distance"]
    }

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=body,
        headers=headers,
        timeout=120
    )

    response.raise_for_status()

    return response.json()["distances"]