import glob
import os

def get_latest_file(files_folder, files_name):
    # eg: files_folder = "data/raw" files_name = "/products_raw_*.csv"
    files = glob.glob(files_folder + files_name)
    if not files:
        raise FileNotFoundError("No raw products data files found in {}".format(files_folder))
    return max(files, key=os.path.getctime)
