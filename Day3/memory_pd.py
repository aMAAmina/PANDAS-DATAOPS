import pandas as pd 
import os
from utils import data_helper

# Get the absolute path to the "shein-data/raw" directory
# Directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))  
raw_data_dir = os.path.join(base_dir, "../Day2/shein-data/raw")  
data_raw_path = data_helper.get_latest_file(raw_data_dir,"/products_raw_*.csv")

products_df = pd.read_csv(data_raw_path)
products_df.info()
memory_usage = products_df.memory_usage(deep=True)
top3_cons_col = memory_usage[1:].sort_values(ascending=False).head(3)
print(f"- Memory usage of data frame is: {memory_usage.sum()/1024} KB")
print(f"- The top 3 memory-consuming columns:\n{top3_cons_col}")
