import pandas as pd
import requests
import os
import time
from datetime import datetime

print("Shein data loading...")
url = "https://raw.githubusercontent.com/luminati-io/eCommerce-dataset-samples/refs/heads/main/shein-products.csv"
max_retries = 5
delay = 1
retries = 0

while retries < max_retries:
    try:
        print(f"Attempt {retries + 1} to fetch products info...")
        response = requests.get(url)
        response.raise_for_status()
        os.makedirs("shein-data/raw", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M")
        file_path = f"shein-data/raw/products_raw_{timestamp}.csv"
        with open(file_path, "wb") as f:
            f.write(response.content)
        # Load the CSV file using pandas
        products_df = pd.read_csv(file_path, encoding="ISO-8859-1")
        # Rename columns to lowercase with underscore
        products_df.columns = products_df.columns.str.lower().str.replace(" ", "_")
        # Drop any rows with null product names or prices
        products_df.dropna(subset=["product_name", "initial_price", "final_price"], inplace=True)
        # Convert prices to float and ensure non-negatives
        products_df["initial_price"] = products_df["initial_price"].astype(float)
        products_df = products_df[products_df["initial_price"] >= 0]
        products_df["final_price"] = products_df["final_price"].astype(float)
        products_df = products_df[products_df["final_price"] >= 0]
        # Export the dataset as a parquet
        os.makedirs("shein-data/processed", exist_ok=True)
        file_pathf = f"shein-data/processed/products_cl_{timestamp}.parquet"
        products_df.to_parquet(file_pathf, index=False)
        lines = [
            "Data loaded successfully:",
            f"number of rows is {len(products_df)}",
            f"number of columns is {len(products_df.columns)}",
            f"memory usage is {products_df.memory_usage(deep=True).sum()} bytes"
        ]
        for line in lines:
            print(line)
        print(products_df.head())
        success = True
        break

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}. Retrying in {delay} seconds...")
        time.sleep(delay)
        retries += 1
        delay *= 2
if not success:
    raise Exception("Failed to fetch data after multiple retries.")