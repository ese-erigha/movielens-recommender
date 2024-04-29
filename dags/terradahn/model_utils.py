import os

import neptune
import pickle

neptuneAPIKey = "eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0Y2MzNTlkNC04NTExLTRkMWUtYTU4ZC00OTQxYzE5Y2JjYjYifQ=="

def init_neptune_model(name, project):
    model_version = neptune.init_model_version(
        model=name,
        project=project,
        api_token=neptuneAPIKey, # your credentials
    )

    return model_version

def save_to_pickle(model, file_path):
    pickle.dump(model, os.open(file_path, 'wb'))
