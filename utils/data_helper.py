import pandas as pd

def downcast_df(df):
    memory_df = df.memory_usage(deep=True).sum()/1024**2
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

    memory_saved = memory_df - df.memory_usage(deep=True).sum()/1024**2
    return df, memory_saved
