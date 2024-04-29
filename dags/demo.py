import os
import logging
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
        neptune_key = os.getenv('NEPTUNE_API_KEY')
        logging.info("Executed using Apache Airflow ✨ -------------"+neptune_key)

    test_airflow()


    

