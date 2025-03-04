import xml.etree.ElementTree as ET
from structures import WikiPage
from typing import Iterable


FILE_PATH = "/home/tadej/programming/search_engine/enwiki-20250201-pages-articles-multistream.xml.bz2"



import bz2
import xml.etree.ElementTree as ET

def iter_wiki_pages(file_path) -> Iterable[WikiPage]:
    """
    Iterates over Wikipedia pages in a bz2-compressed XML dump.
    Yields a tuple: (title, url, text).
    """
    # Open the file in binary mode
    with bz2.open(file_path, 'rb') as f:
        # Create an iterator that triggers on the end event of elements
        # Note: The XML dump uses namespaces; the '{*}' is a wildcard for any namespace.
        context = ET.iterparse(f, events=('end',))
        for event, elem in context:
            # Check for the page element (may have a namespace prefix)
            if elem.tag.endswith('page'):
                # Extract title
                title_elem = elem.find('./{*}title')
                title = title_elem.text if title_elem is not None else None

                # Extract the text from the revision/text element
                revision = elem.find('./{*}revision')
                text_elem = revision.find('./{*}text') if revision is not None else None
                text = text_elem.text if text_elem is not None else None
                
                # Skip redirects / corrupted
                if text is None:
                    continue
                assert isinstance(text, str)
                if text.startswith("#REDIRECT"):
                    continue

                # Construct a simple URL using the title (replace spaces with underscores)
                url = f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}' if title else None

                # Yield the information for this page
                yield WikiPage(title, url, text)

                # It's important to clear the element to free memory
                elem.clear()

# Example usage:
if __name__ == '__main__':
    #file_path = 'enwiki-latest-pages-articles-multistream.xml.bz2'
    i = 0
    for title, url, text in iter_wiki_pages(FILE_PATH):
        if i == 5:
            break
        else:
            i += 1
        
        print(f"article {i}\n----------------------------------\n")

        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Content snippet: {text[:2000] if text else 'No text available...'}\n")


