from datetime import datetime
import os

import pandas as pd
from airflow import DAG
from airflow.decorators import task
from airflow.decorators import task_group
from airflow.operators.python import PythonOperator

from terradahn import file_utils, dataset_utils, db_utils, svdpp_model, tfidf_model

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow/')
dataset_path = f'{AIRFLOW_HOME}/dags/dataset/'
model_path = f'{AIRFLOW_HOME}/dags/models/'

# dataset remote url
movies_dataset_url = "https://github.com/ese-erigha/movielens-recommender/blob/main/dataset/movies.csv"
ratings_dataset_url = "https://github.com/ese-erigha/movielens-recommender/blob/main/dataset/ratings.csv"

# file path to save dataset
movies_dataset_path = f'{dataset_path}movies.csv'
ratings_dataset_path = f'{dataset_path}ratings.csv'

# file path to save model
svdpp_model_path = f'{model_path}svd_model.pkl'
tfidf_linear_kernel_model_path = f'{model_path}tfidf_linear_kernel.pkl'

fetch_movies_dataset_task_input = {"url": movies_dataset_url, "file_path": movies_dataset_path}

with DAG(
        dag_id="movielens_recommender_dag",
        start_date=datetime(2024, 1, 1),
        schedule="@once"
) as dag:
    @task_group()
    def fetch_datasets():
        fetch_ratings_task = PythonOperator(
            task_id="fetch_ratings_task",
            python_callable=file_utils.save_dataset,
            op_kwargs={"url": ratings_dataset_url, "file_path": ratings_dataset_path}
        )

        fetch_movies_task = PythonOperator(
            task_id="fetch_movies_task",
            python_callable=file_utils.save_dataset,
            op_kwargs={"url": movies_dataset_url, "file_path": movies_dataset_path}
        )

        [fetch_ratings_task, fetch_movies_task]


    @task_group()
    def create_users():
        create_users_table_task = PythonOperator(
            task_id="create_users_table_task",
            python_callable=db_utils.create_users_table
        )

        insert_users_task = PythonOperator(
            task_id="insert_users_task",
            python_callable=dataset_utils.insert_users_into_table,
            op_kwargs={"dataset_path": ratings_dataset_path}
        )

        create_users_table_task >> insert_users_task


    @task_group
    def create_movies():
        create_movies_table_task = PythonOperator(
            task_id="create_movies_table_task",
            python_callable=db_utils.create_movies_table
        )

        insert_movies_task = PythonOperator(
            task_id="insert_movies_task",
            python_callable=dataset_utils.insert_movies_into_table,
            op_kwargs={"movies_dataset_path": movies_dataset_path, "ratings_dataset_path": ratings_dataset_path}
        )

        create_movies_table_task >> insert_movies_task


    @task_group
    def build_models():
        build_svdpp_model_task = PythonOperator(
            task_id="build_svdpp_model_task",
            python_callable=svdpp_model.build_model,
            op_kwargs={"ratings_dataset_path": ratings_dataset_path, "movies_dataset_path": movies_dataset_path, "model_path": svdpp_model_path}
        )

        build_tfidf_model_task = PythonOperator(
            task_id="build_tfidf_model_task",
            python_callable=tfidf_model.build_model,
            op_kwargs={"dataset_path": movies_dataset_path, "model_path": tfidf_linear_kernel_model_path}
        )

        [build_svdpp_model_task, build_tfidf_model_task]

    # fetch_datasets() >> [create_users(), create_movies()] >> build_models()

    # Expose Recommender systems API
    # Create FastAPI services
    # Get by user_id, size, page_number
    # If user exists in the ratings dataframe
    # return paginated response
    # Else
    # return top rated movies

    # Get by movie_id, size, page_number
    # return similar movies using content_based_recommender
