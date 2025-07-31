import pandas as pd
import glob
import os

def get_latest_raw_file():
    files = glob.glob("shein-data/raw/products_raw_*.csv")
    if not files:
        raise FileNotFoundError("No raw products data files found in shein-data/raw/")
    return max(files, key=os.path.getctime)

raw_path = get_latest_raw_file()
products_df = pd.read_csv(raw_path, encoding="ISO-8859-1")

# Data inspection
print(products_df.head(10))
# Columns of data
print("Column names:", products_df.columns)
# Checks if there is an electronics category in the column 'category'
print("Contains 'electronics':", "electronics" in products_df["category"].str.lower().unique())
# Search 'electronis' across all columns
electronics_rows = products_df.apply(lambda col: col.astype(str).str.contains("electronics", case=False, na=False)).any(axis=1)
# 'category' column for matching electronic_rows
category_electronics = products_df.loc[electronics_rows, "category"].unique()
price_electronics = products_df.loc[electronics_rows, "initial_price"]
print(category_electronics)


# Extract all rows where the category matches electronics and the price is in the range
products_df = products_df[
    (products_df["category"].str.lower().isin(category_electronics)) & 
    (products_df["initial_price"] > 10) & 
    (products_df["initial_price"] < 80)
]

products_df = products_df[["product_id", "initial_price", "in_stock", "category"]]

products_df = products_df.sort_values(by="initial_price", ascending=False)
print(products_df.head(10))