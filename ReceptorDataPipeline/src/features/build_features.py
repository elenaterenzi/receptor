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

    df = combine_files_to_df(raw_data_dir)
    #print(len(df))
    df_features = build_features(df)
    #print(len(df_features))
    # print(df_features)

    #df_features.to_csv(out_file)


def combine_files_to_df(dir_path):
    all_files = glob.glob(dir_path + "/*.csv")
    df_all = pd.DataFrame()
    list_ = []
    for file_ in all_files:
        df = pd.read_csv(file_,index_col=None, header=0)
        # Add receipt_id column equal to the file name
        file_name = os.path.basename(file_)
        df["receipt_id"] = file_name
        list_.append(df)
    df_all = pd.concat(list_)
    return(df_all)


def build_features(df):
    df = normalize_coordinates(df)
    return(df)


def normalize_coordinates(df):
    """ 
    Appends columns which contains normalized x,y coordinates
    """

    # heighest_point is max(y1, y2)
    # rightmost_point is max(x2, x3)
    df_max = df.groupby("receipt_id")["receipt_id", "y1", "y2", "x2", "x3"]\
        .transform(max)\
        .set_index('receipt_id')
    df_max["heighest_point"] = df_max[["y1", "y2"]].max(axis=1)
    df_max["rightmost_point"] = df_max[["x2", "x3"]].max(axis=1)
    df_max = df_max.drop(["y1", "y2", "x2", "x3"], axis=1)

    # lowest_point is min(y4, y3)
    # rightmost_point is max(x2, x3)
    df_min = df.groupby("receipt_id")["receipt_id", "y3", "y4", "x1", "x4"]\
        .transform(min)\
        .set_index('receipt_id')
    df_min['lowest_point'] = df_min[["y3", "y4"]].max(axis=1)
    df_min['leftmost_point'] = df_min[["x1", "x4"]].max(axis=1)
    df_min = df_min.drop(["y3", "y4", "x1", "x4"], axis=1)

    # Join back to the original dataset (index = receipt_id)
    df = df.set_index('receipt_id').join(df_max).join(df_min)

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
