import pandas as pd

# Read the Excel file we just created
df = pd.read_excel("data/crypto_data.xlsx")

# Print the first five rows to confirm
print(df.head())