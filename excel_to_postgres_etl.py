import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Resolve base paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DIR = os.path.join(BASE_DIR, "data", "excel_files")
PLACEHOLDER = os.path.join(EXCEL_DIR, "placeholder.xlsx")
DB_URL_ENV = os.getenv("POSTGRES_URL",
                       "postgresql://username:password@localhost:5432/etl_database.db")

# 2. Ensure the excel_files/ directory exists
os.makedirs(EXCEL_DIR, exist_ok=True)

# 3. If no .xlsx files are present, generate a placeholder
if not any(f.endswith(".xlsx") for f in os.listdir(EXCEL_DIR)):
    print(f"[Info] No Excel files found in {EXCEL_DIR}. Generating placeholder.xlsx")
    df = pd.DataFrame({
        "product_id": [1, 2, 3],
        "sales": [100.0, 150.5, 200.75],
        "region": ["North", "East", "West"]
    })
    df.to_excel(PLACEHOLDER, index=False)
    print(f"[Info] Placeholder data written to {PLACEHOLDER}")


# Extract
def extract_excel_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]
    all_data = pd.DataFrame()
    for file in files:
        path = os.path.join(folder_path, file)
        print(f"[Extract] Reading {path}")
        df = pd.read_excel(path)
        all_data = pd.concat([all_data, df], ignore_index=True)
    return all_data


# Transform
def transform_excel_data(df):
    print("[Transform] Cleaning column names and dropping duplicates")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    print(f"[Transform] Dropped {before - after} duplicate rows")
    return df


# Load
def load_to_postgresql(df, db_url, table_name):
    print(f"[Load] Connecting to database: {db_url}")
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"[Load] Wrote {len(df)} records to table `{table_name}`")


if __name__ == "__main__":
    print("=== ETL: Excel ➔ PostgreSQL ===")
    combined = extract_excel_files(EXCEL_DIR)
    cleaned = transform_excel_data(combined)

    # Preview the cleaned data
    print("\n[Preview] First 5 rows:")
    print(cleaned.head(), "\n")

    load_to_postgresql(cleaned, DB_URL_ENV, "aggregated_sales_data")
    print("ETL complete.")
