import pandas as pd
import numpy as np
from utils import data_helper

#Generate a data frame
df = pd.DataFrame({
    'customer_id': np.random.randint(1, 1_000_000, 1_000_000),
    'age': np.random.randint(18, 90, 1_000_000),
    'price': np.random.uniform(1, 500, 1_000_000),
    'city': np.random.choice(['Paris', 'London', 'Berlin', 'Madrid'], 1_000_000),
    'is_active': np.random.choice([True, False], 1_000_000)
})
# Make it inefficient on purpose
df['is_active'] = df['is_active'].astype(object)


memory_df = df.memory_usage(deep=True).sum()/1024**2
print (f"original df mem: {memory_df:.2f}MB")
"""
# Downcasting
df['customer_id'] = pd.to_numeric(df['customer_id'], downcast='unsigned')
df['age'] = pd.to_numeric(df['age'], downcast='unsigned')
df['price'] = pd.to_numeric(df['price'], downcast='float')
# Convert city to a category
df['city'] = df['city'].astype('category')
"""
df, memory_saved = data_helper.downcast_df(df)
print(f"Memory saved by downcasting: {memory_saved:.2f} MB")
# Convert is_active to a bool
df['is_active'] = df['is_active'].astype('bool')
memory_df = df.memory_usage(deep=True).sum()/1024**2
print (f"final df mem: {memory_df:.2f}MB")

