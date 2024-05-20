import logging
import os

import pickle
import neptune
from neptune.utils import stringify_unsupported
from neptune.exceptions import NeptuneException, ModelNotFound

from .config import settings


def save_to_pickle(model, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb') as file:
        pickle.dump(model, file)


def save_to_neptune(model_config: dict):

    try:
        model_version = neptune.init_model_version(
            model=settings.neptune_config.project_key+"-"+model_config["model_key"],
            api_token=settings.neptune_config.api_key,
            project=model_config["project_name"],
        )

        if (model_config.get("model_path") is not None):
            model_version["model/binary"].upload(model_config["model_path"])

        if (model_config.get("rmse") is not None):
            model_version["validation/rmse"] = model_config["rmse"]

        model_version["model/parameters"] = stringify_unsupported(model_config["model_info"])

        model_version.stop()

    except ModelNotFound:

        model = neptune.init_model(
            key=model_config["model_key"],  # Must be uppercase and unique within the project
            name=model_config["model_name"],  # Optional
            project=model_config["project_name"],
            api_token=settings.neptune_config.api_key,
        )

        if(model_config.get("model_path") is not None):
            model["model/signature"].upload(model_config["model_path"])

        if(model_config.get("rmse") is not None):
            model["validation/rmse"] = model_config["rmse"]

        model["model"] = stringify_unsupported(model_config["model_info"])

        model.stop()

    except Exception as err:
        logging.error(err)
