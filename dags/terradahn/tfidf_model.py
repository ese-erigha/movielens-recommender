from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.model_selection import GridSearchCV
import pandas as pd

from .model_utils import save_to_pickle, init_neptune_model
from .config import neptune_config


def clean_data(movies):
    # Determine the number of movies without genres
    # r,c = movies[movies['genres']=='(no genres listed)'].shape
    # print('The number of movies which do not have info about genres:',r)

    # Remove the movies without genre information and reset the index
    # ~ means bitwise not, inversing boolean mask - Falses to Trues and Trues to Falses
    # Essentially, returns all movies with genres
    movies = movies[~(movies['genres']=='(no genres listed)')].reset_index(drop=True)

    # Remove '|' in the genres column
    movies['genres_cleaned'] = movies['genres'].str.replace('|',' ')

    # Change 'Sci-Fi' to 'SciFi' and 'Film-Noir' to 'Noir'
    movies['genres_cleaned'] = movies['genres_cleaned'].str.replace('Sci-Fi','SciFi')
    movies['genres_cleaned'] = movies['genres_cleaned'].str.replace('Film-Noir','Noir')
    
    return movies



def build_model(dataset_path, model_path):
    """

    Function to build SVD++ model

    Parameters:
    dataset_path (str): file path to location of the movies dataset
    model_path (str): pickle file path to store built model

    Returns:
    None

    """
    movies_df = pd.read_csv(dataset_path)
    movies_df = clean_data(movies_df)

    # Build tf-idf vectorizer
    tfidf_vector = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vector.fit_transform(movies_df['genres_cleaned'])

    # create the cosine similarity matrix
    sim_matrix = linear_kernel(tfidf_matrix,tfidf_matrix)

    # Save model to pickle
    model_utils.save_to_pickle(sim_matrix, model_path)

    # Save model to Neptune.ai
    model_name = neptune_config["project_key"]+'-'+'TFIDF'
    neptune_model = model_utils.init_neptune_model(model_name, neptune_config["project_name"])
    neptune_model["model/parameters"] = tfidf_vector.get_params()
    neptune_model["model/binary"].upload(model_path)
    neptune_model.stop()
    
