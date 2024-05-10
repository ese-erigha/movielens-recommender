import os
from pydantic import (
    BaseModel, BaseSettings
)


class NeptuneConfig(BaseModel):
    api_key: str = os.getenv('NEPTUNE_API_KEY')
    project_key: str = "MOVIELENS"
    project_name: str = "ese.erigha/movielens-recommender"


class PostgresConfig(BaseModel):
    user: str = os.getenv('POSTGRES_USER')
    password: str = os.getenv('POSTGRES_PASSWORD')
    database: str = os.getenv('POSTGRES_DB')


class TableNames(BaseModel):
    user: str = "users"
    movie: str = "movies"
    cbr: str = "cbr_predictions"
    svdpp: str = "svdpp_predictions"


class Settings(BaseSettings):
    neptune_config: NeptuneConfig = NeptuneConfig()
    postgres_config: PostgresConfig = PostgresConfig()
    table: TableNames = TableNames()


settings = Settings()

table_names = dict(
    user="users",
    movie="movies",
    cbr="cbr_predictions",
    svdpp="svdpp_predictions"
)
