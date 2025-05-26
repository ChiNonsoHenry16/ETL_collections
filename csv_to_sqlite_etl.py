import os
import pandas as pd
import sqlite3
import seaborn as sns  # for generating Iris dataset if needed

# 1. Determine paths relative to this script file
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
CSV_PATH   = os.path.join(DATA_DIR, "sample_data.csv")
SQLITE_DB  = os.path.join(DATA_DIR, "etl_database.db")

# 2. Ensure data/ directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# 3. If sample_data.csv is missing, generate it via Iris dataset
if not os.path.exists(CSV_PATH):
    print(f"[Info] '{CSV_PATH}' not found; generating Iris sample CSV.")
    iris = sns.load_dataset("iris")
    iris.to_csv(CSV_PATH, index=False)
    print(f"[Info] Sample data written to {CSV_PATH}")

# Extract
def extract_csv(file_path):
    return pd.read_csv(file_path)

# Transform
def transform_data(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df.dropna(inplace=True)
    return df

# Load
def load_to_sqlite(df, db_path, table_name):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    df_raw    = extract_csv(CSV_PATH)
    df_clean  = transform_data(df_raw)
    load_to_sqlite(df_clean, SQLITE_DB, "cleaned_data")
    print("ETL process completed successfully.")
