neptune_config = dict(
    api_key = os.getenv('NEPTUNE_API_KEY')
)

postgres_config = dict(
    user = os.getenv('POSTGRES_USER'),
    password = os.getenv('POSTGRES_PASSWORD'),
    database = os.getenv('POSTGRES_DB'),
)
