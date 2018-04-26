import os
import logging
import dotenv
import glob
import pandas as pd


def main(project_dir):
    logger = logging.getLogger(__name__)

    # Build paths
    raw_data_dir = os.path.join(project_dir, "data", "raw")
    interim_data_dir = os.path.join(project_dir, "data", "interim")
    out_file = os.path.join(interim_data_dir, "features.csv")

    df = combine_files_to_df(raw_data_dir, ".csv")
    df_features = build_features(df)

    # Write out
    if not os.path.exists(interim_data_dir):
        os.makedirs(interim_data_dir)
    df_features.to_csv(out_file)


def combine_files_to_df(dir_path, file_extension):
    """ 
    Combines CSV files into a single Pandas Dataframe
    """
    logger = logging.getLogger(__name__)
    logger.info("Combinding files ending in %(file_extension)s in %(dir_path)s into a Pandas Dataframe" % {"file_extension": file_extension, "dir_path": dir_path})

    all_files = glob.glob(dir_path + "/*" + file_extension)
    df_all = pd.DataFrame()
    list_ = []
    for file_ in all_files:
        df = pd.read_csv(file_)
        # Add receipt_id column equal to the file name
        df['id'] = df.index
        file_name = os.path.basename(file_)
        df["receipt_id"] = file_name
        df = df.set_index(["receipt_id", "id"])
        list_.append(df)
    df_all = pd.concat(list_)
    return(df_all)


def build_features(df):
    """ 
    Main method. Builds features (appends columns) to the dataframe (df)
    """
    logger = logging.getLogger(__name__)
    logger.info("Building Features...")

    df = normalize_coordinates(df)
    
    return(df)


def normalize_coordinates(df_in):
    """ 
    Appends columns which contains normalized x,y coordinates
    """
    logger = logging.getLogger(__name__)
    logger.info("Normalizing coordinates...")

    # Set index and preserve incremental id
    #df_in = df_in.rename(columns = {"Unnamed: 0": "id"})
    #df_in = df_in.set_index(["receipt_id", "id"])

    # heighest_point is max(y1, y2)
    # rightmost_point is max(x2, x3)
    df_max = df_in.groupby("receipt_id")["y1", "y2", "x2", "x3"].transform(max)
    df_max["heighest_point"] = df_max[["y1", "y2"]].max(axis=1)
    df_max["rightmost_point"] = df_max[["x2", "x3"]].max(axis=1)
    df_max = df_max.drop(["y1", "y2", "x2", "x3"], axis=1)

    # lowest_point is min(y4, y3)
    # rightmost_point is max(x2, x3)
    df_min = df_in.groupby("receipt_id")["y3", "y4", "x1", "x4"].transform(min)
    df_min['lowest_point'] = df_min[["y3", "y4"]].max(axis=1)
    df_min['leftmost_point'] = df_min[["x1", "x4"]].max(axis=1)
    df_min = df_min.drop(["y3", "y4", "x1", "x4"], axis=1)

    # Join back to the original dataset.
    # Join will default to index
    df = df_in.join(df_max).join(df_min)
    df = df.drop(columns=["Unnamed: 0"])

    # Calculate relative coordinates
    df["x1_rel"] = (df["x1"] - df["leftmost_point"]) / (df["rightmost_point"] - df["leftmost_point"])
    df["y1_rel"] = (df["y1"] - df["lowest_point"]) / (df["heighest_point"] - df["lowest_point"])

    df["x2_rel"] = (df["x2"] - df["leftmost_point"]) / (df["rightmost_point"] - df["leftmost_point"])
    df["y2_rel"] = (df["y2"] - df["lowest_point"]) / (df["heighest_point"] - df["lowest_point"])

    df["x3_rel"] = (df["x3"] - df["leftmost_point"]) / (df["rightmost_point"] - df["leftmost_point"])
    df["y3_rel"] = (df["y3"] - df["lowest_point"]) / (df["heighest_point"] - df["lowest_point"])

    df["x4_rel"] = (df["x4"] - df["leftmost_point"]) / (df["rightmost_point"] - df["leftmost_point"])
    df["y4_rel"] = (df["y4"] - df["lowest_point"]) / (df["heighest_point"] - df["lowest_point"])

    return(df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Get project directory
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

    # Load dotenv
    dotenv_path = os.path.join(project_dir, '.env')
    dotenv.load_dotenv(dotenv_path)
    
    # Run
    main(project_dir)
