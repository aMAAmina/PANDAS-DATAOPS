import pandas as pd
from utils import os_utils

# Get the absolute path to the "shein-data/raw" directory 
raw_data_dir = os_utils.abs_ff_path("../data/shein-data/raw")

raw_path = os_utils.get_latest_file(raw_data_dir, "/products_raw_*.csv")
products_df = pd.read_csv(
    raw_path, 
    encoding="ISO-8859-1",
    dtype={
        "initial_price":"float32",
        "final_price":"float32",
        "product_name":"string",
        "description":"string", 
        "currency":"string",
        "in_stock":"bool",
        "color":"string",
        "size":"string",
        "reviews_count":"int32",
        "main_image":"string",
        "category_url":"category",
        "url":"string",
        "category_tree":"string",
        "country_code":"string",
        "domain":"string",
        "image_count":"int32",
        "image_urls":"string", 
        "model_number":"string", 
        "offers":"string",
        "other_attributes":"string",
        "product_id":"string",
        "rating":"int32",
        "related_products":"string", 
        "root_category":"category",
        "top_reviews":"string",
        "category":"category", 
        "brand":"category", 
        "all_available_sizes":"string"
    })

# Data inspection
print(products_df.head())
print(products_df.tail())
print(f"The data contains :{len(products_df)}")
#'color' is missing 63 values, 'offers', 'related_products', 'top_reviews' are missing 1000 values (100%)
print(f"Nulls: {products_df.isnull().sum()}")
products_df.drop(columns=["offers", "top_reviews", "related_products"], inplace=True)
print("Columns 'offers', 'related_products', 'top_reviews' dropped.")

# Columns of data
print("Column names:", products_df.columns)

# Drop duplicate products by product_id, keep the first occurrence
products_df.drop_duplicates(subset=["product_id"], inplace=True)
products_df.reset_index(drop=True, inplace=True)
print("Duplicates dropped and index reset.")
#sort by final_price
products_df = products_df.sort_values(by="final_price", ascending=False)
print("After sorting:")
print(products_df[["product_name","final_price"]].head())

#drop duplicates
Pd_len = len(products_df)
print(f"Prior dropping df conatins : {len(products_df)} rows")
products_df.drop_duplicates(subset=["model_number"], keep="last", inplace=True)
Ad_len = len(products_df)
if Pd_len - Ad_len > 0:
    print(f"Dropped : {Pd_len - Ad_len} rows")
else:
    print("No duplicates found.")

# Checks if there is an electronics category in the column 'category'
print("Contains 'electronics':", "electronics" in products_df["category"].str.lower().unique())

# Debug: Check for laptops in the original DataFrame
laptops_orig = products_df[products_df["category"].str.lower() == "laptops"]
print("Laptops in original DataFrame:")
print(laptops_orig.head())
print("Laptops price stats (original):")
print(laptops_orig["initial_price"].describe())
if "rating" in laptops_orig.columns:
    print("Laptops rating stats (original):")
    print(laptops_orig["rating"].describe())
else:
    print("No 'rating' column in laptops_orig")

# Set product_id as index and extract one row by ID
laptops_df = laptops_orig.set_index("product_id")

if not laptops_df.empty:
    example_id = laptops_df.index[0]
    print(f"Row for product_id {example_id}:")
    print(laptops_df.loc[example_id])

# Search 'electronis' across all columns
electronics_rows = products_df.apply(lambda col: col.astype(str).str.contains("electronics", case=False, na=False)).any(axis=1)

# 'category' column for matching electronic_rows
category_electronics = products_df.loc[electronics_rows, "category"].unique()
price_electronics = products_df.loc[electronics_rows, "initial_price"]
print(f"price_electronics {price_electronics}")
print(f"category_electronics {category_electronics}")

#know the root_category of every category in category_electronics
for cat in category_electronics:
    cat_rows = products_df[products_df["category"] == cat]
    root_cats = cat_rows["root_category"].unique()
    print(f"Category: {cat} -> Root categories: {root_cats}")

print("Extract all rows where the category matches electronics and the price is in the range")
products_df = products_df[
    (products_df["category"].str.lower().isin(category_electronics)) & 
    (products_df["initial_price"] > 10) & 
    (products_df["initial_price"] < 2000)
]
print(products_df)

#Empty DataFrame
print("Debug: Show laptops before rating filter")
laptops_all = products_df[products_df["category"].str.lower() == "laptops"]
print(laptops_all.head())

print("Laptops rating stats:")
if "rating" in laptops_all.columns:
    print(laptops_all["rating"].describe())
else:
    print("No 'rating' column in laptops_all")
print("Laptops initial_price stats:")
print(laptops_all["initial_price"].describe())
print(products_df[products_df["category"].str.lower() == "laptops"].shape)
print(products_df[products_df["category"].str.lower() == "laptops"].head())
print(products_df.columns)

print("Filter for all products in (Laptops) with a rating above 4.5 and initial_price below $1000")
laptops_df = products_df[
    (products_df["category"].str.lower() == "laptops") &
    (products_df["rating"] >= 4.5) &
    (products_df["initial_price"] < 1000)
]
print(laptops_df.head())
print(products_df.columns)

products_df = products_df[["product_id", "initial_price", "in_stock", "category"]]

products_df = products_df.sort_values(by="initial_price", ascending=False)
print(products_df.head(10))