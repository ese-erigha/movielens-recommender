import logging
import pandas as pd

from .db_utils import insert_dataframe
from .config import settings

def insert_users_into_table(dataset_path):
    logging.info("ratings dataframe path "+ dataset_path)
    ratings_df = pd.read_csv(dataset_path)
    all_users = ratings_df['userId'].unique().tolist()

    data = {'id': all_users}
    df = pd.DataFrame(data)

    insert_dataframe(settings.table.user, df)


def insert_movies_into_table(movies_dataset_path, ratings_dataset_path):
    movies_df = pd.read_csv(movies_dataset_path)
    ratings_df = pd.read_csv(ratings_dataset_path)

    average_movie_ratings = ratings_df.groupby(by='movieId')['rating'].mean().sort_values(ascending=False).reset_index()
    merged_df = movies_df.merge(average_movie_ratings, how='outer')
    merged_df['rating'] = merged_df['rating'].round(1)
    merged_df.rename(columns={"rating": "average_rating", "movieId": "id"}, inplace=True)
    merged_df['average_rating'] = merged_df['average_rating'].fillna(0)

    insert_dataframe(settings.table.movie, merged_df)
