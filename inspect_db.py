#This code is to peak into the database created using Python.

import os
import sqlite3
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "data", "etl_database.db")

# Connect and query
conn = sqlite3.connect(DB_PATH)
df   = pd.read_sql_query("SELECT * FROM cleaned_data LIMIT 5;", conn)
conn.close()

print(df)