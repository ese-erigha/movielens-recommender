from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.decorators import TaskGroup
from airflow.operators.python import PythonOperator

from terradahn import file_utils

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow/')
dataset_path = f'{AIRFLOW_HOME}/dags/dataset/'

# Dataset remote url
movies_dataset_url = "https://github.com/ese-erigha/movielens-recommender/blob/main/dataset/movies.csv"
ratings_dataset_url = "https://github.com/ese-erigha/movielens-recommender/blob/main/dataset/ratings.csv"

# Dataset file path to save
movies_dataset_path = f'{dataset_path}movies.csv'
ratings_dataset_path = f'{dataset_path}ratings.csv'

fetch_movies_task_input = { "url": movies_dataset_url, "file_path": movies_dataset_path }
fetch_ratings_task_input = { "url": ratings_dataset_url, "file_path": ratings_dataset_path }

with DAG(
    dag_id="movielens_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@once"
    ) as dag:

    with TaskGroup("fetch_dataset") as fetch_dataset:
        fetch_movies_task = PythonOperator(
            task_id="fetch_movies", 
            python_callable=file_utils.save_dataset,
            op_kwargs= fetch_movies_task_input
        )
        
        fetch_ratings_task = PythonOperator(
            task_id="fetch_ratings", 
            python_callable=file_utils.save_dataset,
            op_kwargs= fetch_ratings_task_input
        )

        fetch_movies_task >> fetch_ratings_task
    # Fetch movies.csv
        # Save to dataset directory
        # Clean movies
        # Save movies to database table movies - id, index, title, genres, average_rating

    # Fetch ratings.csv
        # Save to dataset directory
        # Compute top rated movies and save to database using https://github.com/hquach/Python-Data-Analysis/blob/master/MovieLens%20Recommendation%20System.ipynb

    # Content_based recommender
        # build model using movies
        # save model to MLFlow

    # Item based recommender
        # build model using ratings
        # save model to MLFLow


    # Expose Recommender systems API
        # Create FastAPI services
            # Get by user_id, size, page_number
                # If user exists in the ratings dataframe
                    # return paginated response
                # Else
                    # return top rated movies

            # Get by movie_id, size, page_number
                # return similar movies using content_based_recommender
