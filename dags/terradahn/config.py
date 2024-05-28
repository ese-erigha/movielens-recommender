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
    dbname: str = os.getenv('POSTGRES_DB')
    host: str = "postgres"


class ExternalDatabaseConfig(BaseModel):
    user: str = "postgres.kfajbfeftfaepqhslhyi"
    password: str = "lexEME5195.."
    dbname: str = "postgres"
    host: str = "aws-0-us-west-1.pooler.supabase.com"


class TableNames(BaseModel):
    user: str = "users"
    movie: str = "movies"
    cbr: str = "cbr_predictions"
    svd: str = "svd_predictions"


class Settings(BaseSettings):
    neptune_config: NeptuneConfig = NeptuneConfig()
    postgres_config: PostgresConfig = PostgresConfig()
    table: TableNames = TableNames()
    external_database_config: ExternalDatabaseConfig = ExternalDatabaseConfig()
    prediction_size: int = 50


settings = Settings()

