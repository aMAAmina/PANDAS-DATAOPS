### Goals:

#### Part1: Memory Optimization & Chunked Processing for Large Datasets
- [memory_pd.py](memory_pd.py) - Analyze memory usage of dataframes
- [downcast_pd.py](downcast_pd.py) - Optimize memory by changing data types:
    (Downcasting: Downcasting is changing a data type to a smaller, more specific variant, without loosing information
    ++ helps reduce memory usage without changing the values or behavior of your data.)
- [chunk_pd.py](chunk_pd.py) - Load and process massive files using chunking strategies:
    (Chunked reading means loading a file in smaller portions (chunks) instead of all at once.
    In pandas it returns an iterator that yields DataFrames of specified chunk size.
    This is useful for large files that cannot fit into memory all at once.)
- [explore_dask.py](explore_dask.py)Apply lazy evaluation techniques for big data
- Build scalable data ingestion pipelines for preprocessing