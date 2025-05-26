import os
import requests
import pandas as pd

# 1. Determine paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_XLS = os.path.join(DATA_DIR, "crypto_data.xlsx")

# 2. Ensure data/ directory exists
os.makedirs(DATA_DIR, exist_ok=True)


# 3. Extract
def extract_api_data(url):
    response = requests.get(url)
    response.raise_for_status()  # fail early on bad HTTP
    data = response.json()
    return pd.json_normalize(data)


# 4. Transform
def transform_api_data(df):
    df = df[['id', 'symbol', 'name', 'current_price', 'market_cap']]
    df.columns = [col.upper() for col in df.columns]
    return df


# 5. Load
def load_to_excel(df, file_path):
    df.to_excel(file_path, index=False)


if __name__ == "__main__":
    api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"

    # Run ETL
    raw_df = extract_api_data(api_url)
    transformed = transform_api_data(raw_df)
    load_to_excel(transformed, OUTPUT_XLS)

    print(f"API data successfully saved to {OUTPUT_XLS}")
