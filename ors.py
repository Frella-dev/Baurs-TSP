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

    if response.status_code != 200:

        raise Exception(
            f"STATUS={response.status_code}\nBODY={response.text}"
        )

    return response.json()["distances"]
