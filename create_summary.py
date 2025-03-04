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
for title, url, text in iter_wiki_pages(file_path):
    # Construct a prompt asking for a one-sentence summary
    prompt = f"Summarize the following content in one sentence:\n\n{text}"

    try:
        # Call the Gemini 2.0 Flash model via the OpenAI API
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            n=1,
        )

        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Summary: {summary}")
        print("-" * 40)
        break

    except Exception as e:
        print(f"An error occurred processing '{title}': {e}")
        break
