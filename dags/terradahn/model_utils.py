import os

import neptune
import pickle

neptuneAPIKey = "eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJjMTk0ZGZmZi1jMzMyLTQ5NDktYjFkYy03Y2JlNDIyY2VjZjEifQ=="

def init_project(key, name):
    model_version = neptune.init_model_version(
        model=key, # project key on neptune
        project=name,
        api_token=neptuneAPIKey, # your credentials
    )

    return model_version

def save_to_pickle(model, file_path):
    pickle.dump(model, os.open(file_path, 'wb'))
