import pandas as pd 
from utils import os_utils

# Get the absolute path to the "shein-data/raw" directory 
raw_data_dir = os_utils.abs_ff_path("../data/shein-data/raw")
data_raw_path = os_utils.get_latest_file(raw_data_dir,"/products_raw_*.csv")

products_df = pd.read_csv(data_raw_path)
products_df.info()
memory_usage = products_df.memory_usage(deep=True)
top3_cons_col = memory_usage[1:].sort_values(ascending=False).head(3)
print(f"- Memory usage of data frame is: {memory_usage.sum()/1024:.2f} KB")
print(f"- The top 3 memory-consuming columns:\n{top3_cons_col}")
