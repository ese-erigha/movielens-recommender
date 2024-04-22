from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="demo_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@once"
    ) as dag:

    @task()
    def test_airflow():
        print("Executed using Apache Airflow ✨")

    test_airflow()

    # Fetch movies.csv
        # Save to dataset directory
        # Clean movies
        # Save movies to database table movies - id, index, title, genres

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
    



    

