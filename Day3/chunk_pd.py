import pandas as pd
import os
from utils import os_utils
from collections import defaultdict

chunksize = 500_000
attack_traffic = defaultdict(float)
attack_counts = defaultdict(int)

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

total_traffic = 0
count_traffic = 0

# Process each chunk
for chunk in reader:
    total_rows += len(chunk)

    # Total data traffic
    if 'IN_BYTES' in chunk.columns and 'OUT_BYTES' in chunk.columns:
        chunk['TOTAL_BYTES'] = chunk['IN_BYTES'] + chunk['OUT_BYTES']
        total_traffic += chunk['TOTAL_BYTES'].sum()

    # Aggregate traffic and counts for each attack type in the current chunk
    grouped_traffic = chunk.groupby('Attack')['TOTAL_BYTES'].sum()
    # Count how many times each unique attack type appears in a column
    grouped_counts = chunk['Attack'].value_counts()
    for attack, total_tr in grouped_traffic.items():
        attack_traffic[attack] += total_tr 
    for attack, count in grouped_counts.items():
        attack_counts[attack] += count  

    # keep only rows where: Attack is Brute Force
    chunk = chunk[chunk['Attack'] == 'Brute Force']
    # Append filtered rows to the output file
    output_dir = os.path.dirname(filtered_path)
    os.makedirs(output_dir, exist_ok=True)
    chunk.to_csv(filtered_path, mode='a', index=False, header=not header_written)
    # Set to True after writing the first chunk
    header_written = True  
    print(f"Chunk shape: {chunk.shape}")
    
# Print the final aggregated traffic for each attack type
print("Final Traffic and Average Traffic by Attack:")
for attack, total_tr in attack_traffic.items():
    count_tr_att = attack_counts[attack]
    mean_tr_att = total_tr / count_tr_att
    print(f"{attack}: Total Traffic = {total_tr}, Average Traffic = {mean_tr_att:.2f}")

#total of rows is: 75987976
print(f"Total number of rows in the dataset: {total_rows}")

