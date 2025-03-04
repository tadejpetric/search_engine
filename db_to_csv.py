import pickle
from create_db import Entry, Database
import csv

with open("database.pkl", "rb") as pkl_db:
    database: Database = pickle.load(pkl_db)

with open("database.csv", "w") as csv_db:
    for entry in database.entries:
        emb = entry.embedding[:10]
        csv_db.write(f"{entry.title}, {entry.question}, {entry.url}, {emb}\n")