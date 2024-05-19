import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

from .model_utils import save_to_pickle, save_to_neptune
from .db_utils import insert_dataframe, create_cbr_predictions_table, get_columns_from_dataframe
from .config import settings


def clean_data(movies):
    # Determine the number of movies without genres
    # r,c = movies[movies['genres']=='(no genres listed)'].shape
    # print('The number of movies which do not have info about genres:',r)

    # Remove the movies without genre information and reset the index
    # ~ means bitwise not, inverse boolean mask - False to True and Trues to False
    # Essentially, returns all movies with genres
    movies = movies[~(movies['genres'] == '(no genres listed)')].reset_index(drop=True)

    # Remove '|' in the genres column
    movies['genres_cleaned'] = movies['genres'].str.replace('|', ' ')

    # Change 'Sci-Fi' to 'SciFi' and 'Film-Noir' to 'Noir'
    movies['genres_cleaned'] = movies['genres_cleaned'].str.replace('Sci-Fi', 'SciFi')
    movies['genres_cleaned'] = movies['genres_cleaned'].str.replace('Film-Noir', 'Noir')

    return movies


def save_recommendations(sim_matrix, df, n=100):
    # Create table
    create_cbr_predictions_table()

    for idx, _ in df.iterrows():
        movie_id = df[df.index == idx]['movieId'].values[0]
        logging.info("Started movie --- " + str(movie_id))

        # Get the pairwise similarity scores of all movies with this movie
        sim_scores = list(enumerate(sim_matrix[int(idx)]))

        # exclude the movie and sort the movies based on the similarity scores
        sim_scores = list(filter(lambda x:x[0] != int(idx), sorted(sim_scores,key=lambda x:x[1], reverse=True)))

        # exclude the movie
        # sim_scores = list(filter(lambda x: x[0] != int(idx), sim_scores))

        movie_ids = []
        sim_movie_ids = []
        scores = []
        for item_sim in sim_scores[:n]:
            sim_movie_index = item_sim[0]
            sim_movie_id = df[df.index == sim_movie_index]['movieId'].values[0]
            score = round(item_sim[1], 2)

            movie_ids.append(movie_id)
            sim_movie_ids.append(sim_movie_id)
            scores.append(score)

        # Create a dataframe
        data = {"movie_id": movie_ids, "sim_movie_id": sim_movie_ids, "score": scores}
        new_df = pd.DataFrame(data)

        cols = get_columns_from_dataframe(new_df)
        query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT(movie_id,sim_movie_id) DO NOTHING" % (settings.table.cbr,cols)

        # Insert similar movies into database
        insert_dataframe(settings.table.cbr, new_df, query)
        logging.info("Completed movie --- "+str(movie_id))


def build_model(dataset_path, model_path):
    """

    Function to build SVD model

    Parameters:
    dataset_path (str): file path to location of the movies dataset
    model_path (str): pickle file path to store built model

    Returns:
    None

    """
    movies_df = pd.read_csv(dataset_path)
    movies_df = clean_data(movies_df)

    # Build tf-idf vectorizer
    tfidf_vector = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vector.fit_transform(movies_df['genres_cleaned'])

    # create the cosine similarity matrix
    sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Save similarity matrix to database
    save_recommendations(sim_matrix, movies_df)

    # Save model to pickle
    # save_to_pickle(sim_matrix, model_path)

    # Save model to Neptune.ai
    model_config = {
        "key": 'TFIDF',
        "name": "Content Based Recommender",
        "project": settings.neptune_config.project_name,
        "model_info":  tfidf_vector.get_params(),
    }

    save_to_neptune(model_config)
    # model_name = settings.neptune_config.project_key + '-' + 'TFIDF'
    # neptune_model = init_neptune_model(model_name, settings.neptune_config.project_name)
    # neptune_model["model/parameters"] = tfidf_vector.get_params()
    # # neptune_model["model/binary"].upload(model_path)
    # neptune_model.stop()
