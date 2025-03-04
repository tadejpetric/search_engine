# Wikipedia Search Engine with Question Generation and Embeddings

## Overview
This repository implements a simple search engine that leverages Wikipedia content. It processes Wikipedia pages from a compressed XML dump, automatically generates questions from the page content using a generative language model, computes embeddings for these questions, and finally enables similarity search using a nearest neighbor algorithm.

The project uses:
- **OpenAI's APIs** (Gemini-2.0 Flash for question generation and text-embedding-004 for embeddings)
- **scikit-learn** for the nearest neighbor search
- **NumPy** for numerical operations

## Repository Structure
- **create_db.py**  
  Processes a set of Wikipedia pages, generates questions per page, computes embeddings for each question, and saves the results in a pickle database (`database.pkl`).

- **create_embeddings.py**  
  Contains the `get_embeddings` function which calls the OpenAI API to generate a numerical embedding for a given question.

- **create_questions.py**  
  Generates questions from Wikipedia page content using a prompt sent to the generative model. It also includes a helper function (`parse_text`) to extract questions from the model’s output, where each question is expected to be wrapped in `<question>` tags.

- **iter_test.py**  
  Iterates over a bz2-compressed Wikipedia XML dump. It extracts the title, URL, and content of each page, skipping redirects and pages with missing content.

- **structures.py**  
  Defines the `WikiPage` dataclass to encapsulate the title, URL, and content of a Wikipedia page.

- **search_engine.py**  
  Loads the database, computes an embedding for a user query, and finds the closest matching question (and its associated Wikipedia page) using scikit-learn’s NearestNeighbors algorithm.

## Prerequisites
- Python 3.8 or higher
- Required packages:
  - `openai`
  - `numpy`
  - `scikit-learn`
- A valid OpenAI API key stored in a file named `keys.txt` in the project root.
- A Wikipedia XML dump in bz2 format. Update the file paths in `iter_test.py` and `create_questions.py` if necessary.

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies:**
   Manually install the required packages:
   ```bash
   pip install openai numpy scikit-learn
   ```

## Usage

### 1. Create the Database
Run the `create_db.py` script to process Wikipedia pages, generate questions, compute embeddings, and save them to `database.pkl`:
```bash
python create_db.py
```
This script will:
- Process a specified number of Wikipedia pages (default is 10).
- Generate up to 5 questions per page.
- Save the resulting entries (page title, URL, question, embedding) to a pickle file.

### 2. Search the Database
To search the database for the question most similar to your query, run the `search_engine.py` script with your query:
```bash
python search_engine.py --question "Your search query here"
```
The script will:
- Compute an embedding for your input query.
- Use the Nearest Neighbors algorithm to find the closest matching question in the database.
- Print the matched question, its distance from the query, and the associated Wikipedia page title and URL.

## Design and Algorithm

### Pipeline Overview
1. **Data Extraction:**
   - `iter_test.py` reads a bz2-compressed Wikipedia XML dump.
   - For each Wikipedia page, it extracts the title, URL, and content (ignoring redirects and corrupted pages).

2. **Question Generation:**
   - `create_questions.py` constructs a prompt that includes the Wikipedia page content.
   - It uses the Gemini-2.0 Flash model to generate questions wrapped in `<question>` tags.
   - The helper function `parse_text` extracts these questions from the model’s output.

3. **Embedding Generation:**
   - Each generated question is passed to `create_embeddings.py`, which calls the OpenAI embeddings API to compute a numerical representation (embedding) of the question.

4. **Database Creation:**
   - `create_db.py` aggregates all entries (each with the page title, URL, question, and embedding) into a `Database` dataclass.
   - The database is then serialized and saved to `database.pkl`.

5. **Similarity Search:**
   - `search_engine.py` loads the saved database.
   - A new query is embedded using the same OpenAI API.
   - scikit-learn’s `NearestNeighbors` algorithm (using Euclidean distance) finds the closest matching question embedding in the database.
   - The corresponding Wikipedia page details are returned and displayed.

### Algorithm Details
- **NearestNeighbors Search:**
  - All question embeddings are collected into a NumPy array.
  - The NearestNeighbors model is fit on these embeddings.
  - For a given query embedding, the model finds the closest entry based on Euclidean distance.

- **Error Handling:**
  - Both the question generation and embedding functions include error handling. If an error occurs (e.g., during an API call), the script logs the error and continues processing subsequent entries.

