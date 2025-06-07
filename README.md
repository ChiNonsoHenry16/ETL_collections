# ETL_collections

These are a simple set of Python scripts demonstrating end-to-end Extract → Transform → Load (ETL) workflows for different data sources and targets. The python files have the following names under the ETL_Scripts root: csv_to_sqlite_etl.py, api_to_excel_etl.py, excel_to_postgres_etl.py. There is also a data directory, to allow the creation of the sample_data.csv file. An SQLite database (etl_database.db) is created by Script 1, while Excel file (crypto_data.xlsx) is created by Script 2. Then, Script 3 generates placeholder.xlsx, if it does not exist. 

Prerequisites
1. Python 3.7+ installed (I used Pycharm for the project).
2. A terminal or command prompt.

Optional:
a. PostgreSQL server running locally or via Docker (for Script 3).
b. A free CoinGecko API key (optional—scripts use public endpoints without a key).
