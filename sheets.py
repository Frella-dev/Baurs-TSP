import pandas as pd

def load_sheet(sheet_url):

    csv_url = sheet_url.replace(
        "/edit?usp=sharing",
        "/export?format=csv"
    )

    df = pd.read_csv(csv_url)

    return df