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

    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        raise Exception(
            f"ORS Error {response.status_code}\n{response.text}"
        )

    return response.json()["distances"]
