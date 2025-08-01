import dask.dataframe as dd
from utils import os_utils
from dask.distributed import Client
client = Client(n_workers=2, threads_per_worker=1, memory_limit="1GB")

raw_data_dir = os_utils.abs_ff_path("../data/cyber/network_simulation.csv")  
print(raw_data_dir)
df = dd.read_csv(raw_data_dir, blocksize="100MB")  # Adjust block size to fit your memory
df = df[df['Attack'] == 'Brute Force'] # early filter for mem :'(
# Note: No data is loaded yet!
#print(df.head())  # Triggers a small computation

# Calculate total traffic per attack
df['TOTAL_BYTES'] = df['IN_BYTES'] + df['OUT_BYTES']
tr_attack = df.groupby('Attack')['TOTAL_BYTES'].sum()

# Nothing is computed yet!
result = tr_attack.compute()  # Now Dask does the work
print(result)
