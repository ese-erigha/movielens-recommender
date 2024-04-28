import os

import neptune
import pickle

neptuneAPIKey = "A"

def init_project(key, name):
    model_version = neptune.init_model_version(
        model=key, # project key on neptune
        project=name,
        api_token=neptuneAPIKey, # your credentials
    )

    return model_version

def save_to_pickle(model, file_path):
    pickle.dump(model, os.open(file_path, 'wb'))
