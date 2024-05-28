import logging
import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVD
# from surprise import accuracy
# from surprise.model_selection import train_test_split
from surprise.model_selection import GridSearchCV

from .model_utils import save_to_pickle, save_to_neptune
from .config import settings
from .db_utils import insert_dataframe, create_svd_predictions_table, get_columns_from_dataframe


def save_recommendations(algo, ratings_df, movies_df, n=settings.prediction_size):
    """

        Function to predict recommendations for each user

        Parameters:
        algo (obj): algorithm to be used
        ratings_df (dataframe): ratings dataframe
        movies_df (dataframe): ratings dataframe to build the predictions

        Returns:
        None

    """
    # Get list of all users
    all_users = ratings_df['userId'].unique().tolist()

    # Create table
    create_svd_predictions_table()

    # Loop through all userId in unique users
    for uid in all_users:
        logging.info("Started user --- " + str(uid))
        all_movies = ratings_df['movieId'].unique()
        user_movies = ratings_df[ratings_df['userId'] == uid]['movieId'].unique()
        unrated_movies = list(set(all_movies) - set(user_movies))

        movie_ids = []
        user_ids = []
        scores = []

        # Predict the ratings for the unrated movies
        predictions = [algo.predict(uid, movie_id) for movie_id in unrated_movies]
        predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

        for prediction in predictions[:n]:
            movie = movies_df[movies_df["movieId"] == prediction.iid]
            movie_id = movie['movieId'].values[0]
            score = round(prediction.est, 2)

            movie_ids.append(movie_id)
            user_ids.append(uid)
            scores.append(score)

        # Create a dataframe
        data = {"user_id": user_ids, "movie_id": movie_ids, "score": scores}
        new_df = pd.DataFrame(data)

        cols = get_columns_from_dataframe(new_df)
        query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT(user_id,movie_id) DO NOTHING" % (settings.table.svd, cols)

        # Insert predictions into the database
        insert_dataframe(settings.table.svd, new_df, query)
        logging.info("Completed user --- " + str(uid))


def build_model(ratings_dataset_path, movies_dataset_path, model_path):
    """

    Function to build SVD++ model

    Parameters:
    ratings_dataset_path (str): file path to location of ratings dataset
    movies_dataset_path (str): file path to location of movies dataset
    model_path (str): pickle file path to store built model

    Returns:
    None

    """

    logging.info("Started SVDPP Model building")
    ratings_df = pd.read_csv(ratings_dataset_path)
    movies_df = pd.read_csv(movies_dataset_path)
    reader = Reader(rating_scale=(1.0, 5.0))
    dataset = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    # trainset, _ = train_test_split(dataset, test_size=.25, random_state = 50)

    param_grid = {'n_factors': [200, 250, 300], 'n_epochs': [35, 40, 45], 'lr_all': [0.01, 0.1, 0.2],
                  'reg_all': [0.1, 0.4, 0.6]}

    # https://surprise.readthedocs.io/en/stable/getting_started.html#grid-search-usage-py
    grid_search = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=5, refit=True, n_jobs=-2, joblib_verbose=5)

    logging.info("Building SVD model via GridSearch")

    # Fit the model
    grid_search.fit(dataset)

    algo = grid_search.best_estimator["rmse"]

    # No need to fit since we called refit=True in GridSearchCV
    # algo.fit(trainset)

    logging.info("Saving Recommendation")

    # Create predictions for all users and save into database
    save_recommendations(algo, ratings_df, movies_df)

    logging.info("Save to Pickle")

    # Save model to pickle
    save_to_pickle(algo, model_path)

    # Save model to Neptune.ai
    model_config = {
        "model_key": 'SVD',
        "model_name": "Item-based Recommender (SVD)",
        "project_name": settings.neptune_config.project_name,
        "model_info": grid_search.best_params["rmse"],
        "model_path": model_path,
        "rmse": grid_search.best_score["rmse"],
    }

    logging.info("Save to Neptune")
    save_to_neptune(model_config)

    # Save model to Neptune.ai
    # model_name = settings.neptune_config.project_key + '-' + 'SVD'
    # neptune_model = init_neptune_model(model_name, settings.neptune_config.project_name)
    # neptune_model["model/parameters"] = grid_search.best_params["rmse"]
    # neptune_model["validation/acc"] = grid_search.best_score["rmse"]
    # neptune_model["model/binary"].upload(model_path)
    # neptune_model.stop()
