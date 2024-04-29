import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVDpp
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV

from .model_utils import save_to_pickle, init_neptune_model

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
    dataset = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    trainset = dataset.build_full_trainset()

    param_grid = { 'n_factors': [200, 250, 300], 'n_epochs': [35, 40, 45], 'lr_all':[0.01,0.1, 0.2], 'reg_all':[0.1, 0.4,0.6] }

    # https://surprise.readthedocs.io/en/stable/getting_started.html#grid-search-usage-py
    grid_search = GridSearchCV(SVDpp, param_grid, measures=['rmse','mae'], cv=5)
    grid_search.fit(dataset) 


    # Fit the model
    algo = grid_search.best_estimator["rmse"]
    algo.fit(trainset)

    # Save model to pickle
    model_utils.save_to_pickle(algo, model_path)

    # Save model to Neptune.ai
    model_name = neptune_project_key+'-'+'SVDPP'
    neptune_model = model_utils.init_neptune_model(model_name, neptune_project_name)
    neptune_model["model/parameters"] = grid_search.best_params["rmse"]
    neptune_model["validation/acc"] = grid_search.best_score["rmse"]
    neptune_model["model/binary"].upload(model_path)
    neptune_model.stop()
