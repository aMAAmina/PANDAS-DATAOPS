import pandas as pd
import os
from utils import os_utils
chunksize = 500_000

# Create an iterator
raw_data_dir = os_utils.abs_ff_path("../data/cyber/network_simulation.csv")  
reader = pd.read_csv(raw_data_dir, chunksize=chunksize)
first_chunk = next(reader)

# Data inspection
print(first_chunk.info())

# Inspect unique values in the 'Label' and 'Attack' columns
print("Unique values in 'Label':", first_chunk['Label'].unique())
print("Unique values in 'Attack':", first_chunk['Attack'].unique())

total_rows = 0
filtered_path = os_utils.abs_ff_path("../data/cyber/network_sim_attacks.csv")

# Initialize a flag to track if the header has been written
header_written = False

total_traffick = 0

# Process each chunk
for chunk in reader:
    total_rows += len(chunk)
    # Total data traffic
    if 'IN_BYTES' in chunk.columns and 'OUT_BYTES' in chunk.columns:
        chunk['TOTAL_BYTES'] = chunk['IN_BYTES'] + chunk['OUT_BYTES']
        total_traffick += chunk['TOTAL_BYTES'].sum()
    # keep only rows where: Attack is Brute Force
    chunk = chunk[chunk['Attack'] == 'Brute Force']
    # Append filtered rows to the output file
    output_dir = os.path.dirname(filtered_path)
    os.makedirs(output_dir, exist_ok=True)
    chunk.to_csv(filtered_path, mode='a', index=False, header=not header_written)
    header_written = True  # Set to True after writing the first chunk
    print(f"Chunk shape: {chunk.shape}")
#total of rows is: 75987976
print(f"Total number of rows in the dataset: {total_rows}")

