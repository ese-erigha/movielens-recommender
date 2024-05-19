import os

import neptune
import pickle
from neptune.utils import stringify_unsupported

from .config import settings


def save_to_pickle(model, file_path):
    pickle.dump(model, os.open(file_path, 'wb'))


def save_to_neptune(model_config: dict):
    model = neptune.init_model(
        key=model_config["key"],  # must be uppercase and unique within the project
        name=model_config["name"],  # optional
        project=model_config["project"],
        api_token=settings.neptune_config.api_key,
    )

    if(model_config["model_path"] is not None):
        model["model/signature"].upload(model_config["model_path"])

    if(model_config["rmse"] is not None):
        model["validation/rmse"] = model_config["rmse"]

    model["model"] = stringify_unsupported(model_config["model_info"])

    model.stop()
