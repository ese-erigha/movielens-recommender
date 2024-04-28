from typing import List, Dict, Tuple

import pandas as pd

import db_utils

def insert_users_into_table(dataset_path):
    ratings_df = pd.read_csv(dataset_path)
    all_users = ratings_df['userId'].unique().tolist()

    insert_query = """INSERT INTO users (id) VALUES (%s) ON CONFLICT (id) DO NOTHING"""
    queries: List[Dict[str, tuple]]  = []

    for id in all_users:
        queries.append(dict(command = insert_query, values = (id)))
    
    db = db_utils.Database()
    db.insert_many(queries)
    db.close_connection()
