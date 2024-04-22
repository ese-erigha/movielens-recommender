# movielens-recommender

A recommender system for the movielens dataset. Recommender engine adopts content-based and item-based recommendation

# https://airflow.apache.org/docs/apache-airflow/2.9.0/tutorial/pipeline.html

# https://github.com/hquach/Python-Data-Analysis/blob/master/MovieLens%20Recommendation%20System.ipynb

# Download the docker-compose.yaml file

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Make expected directories and set an expected environment variable

mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize the database

docker-compose up airflow-init

# Start up all services

docker-compose up
