import glob
import os

def get_latest_file(files_folder, files_name):
    # eg: files_folder = "data/raw" files_name = "/products_raw_*.csv"
    files = glob.glob(files_folder + files_name)
    if not files:
        raise FileNotFoundError("No raw products data files found in {}".format(files_folder))
    return max(files, key=os.path.getctime)

def abs_ff_path(rel_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    the_data_dir = os.path.join(base_dir, rel_path)  
    return the_data_dir