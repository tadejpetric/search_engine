

import pickle

from openai import OpenAI
from structures import Database, Entry
from create_embeddings import get_embeddings

from sklearn.neighbors import NearestNeighbors
import numpy as np
from argparse import ArgumentParser

def find_nearest_entry(database: Database, q_embedding: np.ndarray) -> tuple[Entry, np.float32]:
    # Extract embeddings from all entries in the database.
    embeddings = np.array([entry.embedding for entry in database.entries])
    
    # Create and fit a nearest neighbors model.
    nn_model = NearestNeighbors(n_neighbors=1, algorithm='auto', metric='euclidean')
    nn_model.fit(embeddings)
    
    # Reshape q_embedding to a 2D array and find the nearest neighbor.
    distances, indices = nn_model.kneighbors(q_embedding.reshape(1, -1))
    # Retrieve the nearest entry using the index.
    nearest_index = indices[0][0]
    nearest_entry = database.entries[nearest_index]
    
    return nearest_entry, distances[0][0]

# Example usage:
# q_embedding = get_embeddings(question)
# nearest_entry, distance = find_nearest_entry(my_database, q_embedding)
# print(f"Nearest entry title: {nearest_entry.title} (distance: {distance})")

if __name__ == "__main__":
    with open("database.pkl", "rb") as pkl_db:
        database: Database = pickle.load(pkl_db)
    
    with open("keys.txt", "r") as key_file:
        client = OpenAI(
            api_key=key_file.read().strip(),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
    
    parser = ArgumentParser()
    parser.add_argument("--question", type=str)
    args = parser.parse_args()
    
    q_embedding = get_embeddings(args.question, client)

    entry, dist = find_nearest_entry(database, q_embedding)

    print(f"Nearest neighbour was {entry.question} with distance {dist}\nWiki page {entry.title}  || {entry.url}")



