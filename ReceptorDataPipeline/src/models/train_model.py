import os
import logging
import dotenv
import pandas as pd
import sklearn.linear_model as lm
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

def main(project_dir):
    logger = logging.getLogger(__name__)

    # Build paths
    model_dir = os.path.join(project_dir, "models")
    interim_data_dir = os.path.join(project_dir, "data", "interims")
    features_file = os.path.join(interim_data_dir, "features.csv")
    
    # Read features
    df = pd.read_csv(features_file)

    df = df.fillna(0)
    print(df.info())
    print(df.describe())
    # Split
    X_train, X_test, y_train, y_test = split_data(df)

    # Fit model(s)
    logreg_model = train_logreg_model(X_train, y_train)
    #dense_nn_model = train_dense_nn_model(X_train, y_train)

    # Evaluate
    logger.info("Accuracy of logistic regression classifier on test set: {:.2f}".format(logreg_model.score(X_test, y_test)))

    # Save model(s)
    joblib.dump(logreg_model, os.path.join(model_dir, "logreg_model.pkl"))


def split_data(df_in):
    """ 
    Splits the data
    """
    seed = 42
    test_size = 0.3
    
    features = [
        "x1_rel", "y1_rel", "x2_rel", "y2_rel", "x3_rel", "y3_rel", "x4_rel", "y4_rel",
        "text_has_number", "text_is_number", "text_has_year", "text_has_year", "text_has_month", "text_has_day_of_month", "text_has_DMY_or_YMD"]
    X = df_in[features]
    y = df_in['wordexactlabel']
    return(train_test_split(X, y, test_size=test_size, random_state=seed))


def train_logreg_model(X, y):
    """ 
    Trains a Logistic Regression Model
    """
    logger = logging.getLogger(__name__)
    logger.info("Building Logistic Regression Model...")
    
    # Logisitc regresion
    logreg = lm.LogisticRegression()
    logreg.fit(X, y)

    return logreg


def train_dense_nn_model(X, y):
    """ 
    Trains a Logistic Regression Model
    """
    # TODO


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