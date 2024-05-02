import os

neptune_config = dict(
    api_key = os.getenv('NEPTUNE_API_KEY'),
    project_key = "MOVIELENS",
    project_name = "ese.erigha/movielens-recommender",
)

postgres_config = dict(
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    database = os.getenv('POSTGRES_DB'),
)
