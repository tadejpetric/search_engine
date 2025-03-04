

from openai import OpenAI
from structures import WikiPage
from create_questions import get_questions
from iter_test import iter_wiki_pages, FILE_PATH
from create_embeddings import get_embeddings

import numpy as np

import pickle
from dataclasses import dataclass
import logging


logging.basicConfig(level=logging.INFO)

n_wiki_pages = 10
n_question_per_page = 5

@dataclass
class Entry:
    title: str
    url: str
    question: str
    embedding: np.ndarray

@dataclass
class Database:
    entries: list[Entry]



if __name__=="__main__":
    i = 0
    entries: list[Entry] = []
    # Read the API key from keys.txt
    with open("keys.txt", "r") as key_file:
        client = OpenAI(
            api_key=key_file.read().strip(),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )


    for page in iter_wiki_pages(FILE_PATH):
        logging.info(f"Processing {page.name}")
        if i == n_wiki_pages:
            break
        i += 1

        questions = get_questions(page, client)
        questions = questions[:n_question_per_page]

        for question in questions:
            logging.info(f"\tProcessing question {question}")
            embedding = get_embeddings(question, client)
            if embedding is None:
                continue
            entry = Entry(page.name, page.url, question, embedding)
            entries.append(entry)
    db = Database(entries)
    with open("database.pkl", "wb") as pkl_db:
        pickle.dump(db, pkl_db)