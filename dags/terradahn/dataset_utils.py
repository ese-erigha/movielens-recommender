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

    # first_10_rows = df[:10]
    # print(first_10_rows)

    insert_dataframe(settings.table.user, df)


def insert_movies_into_table(movies_dataset_path, ratings_dataset_path, links_dataset_path):
    movies_df = pd.read_csv(movies_dataset_path)
    ratings_df = pd.read_csv(ratings_dataset_path)
    links_df = pd.read_csv(links_dataset_path)

    # Merge the ratings dataset
    average_movie_ratings = ratings_df.groupby(by='movieId')['rating'].mean().sort_values(ascending=False).reset_index()
    merged_df = movies_df.merge(average_movie_ratings, how='outer')
    merged_df['rating'] = merged_df['rating'].round(1)

    # Merge the links dataset
    merged_df = pd.merge(merged_df, links_df, on='movieId')
    merged_df = merged_df.drop(['imdbId'], axis=1)

    merged_df.rename(columns={"rating": "average_rating", "movieId": "id", "tmdbId": "tmdb_id"}, inplace=True)
    merged_df['average_rating'] = merged_df['average_rating'].fillna(0)
    merged_df['tmdb_id'] = merged_df['tmdb_id'].fillna(0)
    merged_df['tmdb_id'] = merged_df['tmdb_id'].apply(lambda x: int(x))

    # first_10_rows = merged_df[:10]
    # print(first_10_rows)

    insert_dataframe(settings.table.movie, merged_df)
