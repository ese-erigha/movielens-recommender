import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVDpp
from surprise import accuracy
from surprise.model_selection import train_test_split

import model_utils

neptune_project_key = "MOVIELENS"
neptune_project_name = "ese.erigha/movielens-recommender"


def build_svd_model(dataset_path, model_path):

    """

    Function to build SVD++ model

    Parameters:
    dataset_path (str): file path to location of dataset
    model_path (str): pickle file path to store built model

    Returns:
    None

    """

    ratings_df = pd.read_csv(dataset_path)
    reader = Reader(rating_scale=(1.0, 5.0))
    data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.25)

    # We can tune the parameters in the future - https://surprise.readthedocs.io/en/stable/getting_started.html#grid-search-usage-py
    algoSVD = SVDpp()
    algoSVD.fit(trainset)
    predictions = algoSVD.test(testset)
    rmse = accuracy.rmse(predictions)

    # Save model to pickle
    model_utils.save_to_pickle(algoSVD, model_path)

    # Save model to Neptune.ai
    neptune_model = model_utils.init_project(neptune_project_key, neptune_project_name)
    neptune_model["model/parameters"] = {
        "algorithm": "svd++",
        "test_data_size": "25%",
    }
    neptune_model["validation/acc"] = rmse
    neptune_model["model/binary"].upload(model_path)
    neptune_model.stop()
