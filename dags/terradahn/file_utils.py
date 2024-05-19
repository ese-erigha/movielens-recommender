import requests
import os


def save_dataset(url, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    response = requests.get(url)

    with open(file_path, "wb") as file:
        file.write(response.content)
