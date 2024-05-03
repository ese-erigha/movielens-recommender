import os

import neptune
import pickle

from .config import neptune_config


def init_neptune_model(name, project):
    model_version = neptune.init_model_version(
        model=name,
        project=project,
        api_token=neptune_config["api_key"],
    )

    return model_version


def save_to_pickle(model, file_path):
    pickle.dump(model, os.open(file_path, 'wb'))
