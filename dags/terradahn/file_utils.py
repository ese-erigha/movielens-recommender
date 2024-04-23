import requests
import os

def save_dataset(url, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    response = requests.request("GET", url)

    with open(file_path, "w") as file:
        file.write(response.text)
