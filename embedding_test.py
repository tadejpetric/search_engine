from iter_test import iter_wiki_pages


from openai import OpenAI


# Read the API key from keys.txt
with open("keys.txt", "r") as key_file:
    client = OpenAI(
        api_key=key_file.read().strip(),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

#models = client.models.list()
#for model in models:
#  print(model.id)

file_path = "/home/tadej/programming/search_engine/enwiki-20250201-pages-articles-multistream.xml.bz2"

# Iterate over Wikipedia pages
    # Construct a prompt asking for a one-sentence summary

try:
    # Call the Gemini 2.0 Flash model via the OpenAI API
    response = client.embeddings.create(
        model="text-embedding-004",
        input="What is anarchism?",
    )

    # Extract the summary from the response
    print(response)
    print("-" * 40)

except Exception as e:
    print(f"Error {e}")
