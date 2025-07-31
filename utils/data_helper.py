import glob
import os
import pandas as pd

def get_latest_file(files_folder, files_name):
    # eg: files_folder = "data/raw" files_name = "/products_raw_*.csv"
    files = glob.glob(files_folder + files_name)
    if not files:
        raise FileNotFoundError("No raw products data files found in {}".format(files_folder))
    return max(files, key=os.path.getctime)

def downcast_df(df):
    numeric_col = df.select_dtypes(include=['number']).columns  
    object_col = df.select_dtypes(include=['object']).columns 
    for col in numeric_col:
        if pd.api.types.is_integer_dtype(df[col]): 
            df[col] = pd.to_numeric(df[col], downcast='unsigned')
        else: 
            df[col] = pd.to_numeric(df[col], downcast='float')

    for col in object_col:
        # Convert to category if unique values are less than 50% of total rows
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')

    return df
