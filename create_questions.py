from typing import Optional
from iter_test import iter_wiki_pages


from openai import OpenAI

from structures import WikiPage


file_path = "/home/tadej/programming/search_engine/enwiki-20250201-pages-articles-multistream.xml.bz2"


def parse_text(text: str) -> Optional[list[str]]:
    """
    Extracts all content between <question> and </question> tags in the given text.
    Returns a list of the inner content if all tags are properly formed and non-nested.
    If any tags are nested, missing, or unmatched, returns None.
    """
    result = []
    pos = 0
    stack = []
    open_tag = "<question>"
    close_tag = "</question>"

    while pos < len(text):
        # Find the next open or close tag
        next_open = text.find(open_tag, pos)
        next_close = text.find(close_tag, pos)

        # Neither tag found: break out of the loop.
        if next_open == -1 and next_close == -1:
            break

        # If an open tag comes before a close tag (or there is no close tag)
        if next_open != -1 and (next_open < next_close or next_close == -1):
            # If we are already inside a question, that's a nested tag.
            if stack:
                return None
            stack.append(next_open)
            pos = next_open + len(open_tag)
        # Else if a closing tag is found before the next open tag
        elif next_close != -1:
            # If there's no corresponding open tag, it's an error.
            if not stack:
                return None
            start = stack.pop() + len(open_tag)
            content = text[start:next_close]
            result.append(content)
            pos = next_close + len(close_tag)

    # If there's an open tag that wasn't closed, return None.
    if stack:
        return None

    return result


def get_questions(wiki_page: WikiPage, client: OpenAI) -> Optional[list[str]]:
    prompt = f"""
{wiki_page.content}
----
The above text is a wikipedia webpage. Your task is to create 10 questions that have an answer written in the text. Do not provide answers to the listed questions. Try to cover as much of the text as possible.

Output your answers in <question> tags like this
<question>...</question>
""".strip()

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
        response_text = response.choices[0].message.content.strip()
        return parse_text(response_text)

    except Exception as e:
        print(f"An error occurred processing '{wiki_page.name}': {e}")
        return None


# Iterate over Wikipedia pages
if __name__ == "__main__":
    for wiki_page in iter_wiki_pages(file_path):
        # Construct a prompt asking for a one-sentence summary
        print(get_questions(wiki_page))
        break
