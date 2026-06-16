import pandas as pd
import re

def load_sheet(sheet_url):

    sheet_id = re.search(
        r"/d/([a-zA-Z0-9-_]+)",
        sheet_url
    ).group(1)

    csv_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv"
    )

    return pd.read_csv(csv_url)
