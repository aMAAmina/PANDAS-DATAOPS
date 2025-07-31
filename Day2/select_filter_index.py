import pandas as pd
import glob
import os
from utils import data_helper

# Get the absolute path to the "shein-data/raw" directory
# Directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))  
raw_data_dir = os.path.join(base_dir, "shein-data/raw")  

raw_path = data_helper.get_latest_file(raw_data_dir, "/products_raw_*.csv")
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