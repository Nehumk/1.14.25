import os
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser
import requests
from bs4 import BeautifulSoup
from collections import Counter


def scrape_text_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text


# URL to scrape
url = "https://en.wikipedia.org/wiki/Colonial_Pipeline_ransomware_attack"
scraped_text = scrape_text_url(url)

# Create a directory to store the index file
if not os.path.exists("dir"):
    os.mkdir("dir")

# Create a schema
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))

# Create an index in the directory
ind = index.create_in("dir", schema)

# Check if the index exists
exists = index.exists_in("dir")
print("Index exists:", exists)

# Add the scraped document to the index
writer = ind.writer()
writer.add_document(title=u"Colonial Pipeline Ransomware Attack", content=scraped_text, path=u"/wiki_content")
writer.commit()

# Ask user for input to search for a word
search_term = input("Enter a word to search for: ")

# Search the document and calculate word frequency
with ind.searcher() as searcher:
    query = QueryParser("content", ind.schema).parse(search_term)
    results = searcher.search(query, terms=True)

    # Process and display results
    if results:
        for r in results:
            print(f"Document: {r['title']}, Score: {r.score}")
            content = r['content']

            # Calculate the frequency of the searched term
            words = content.split()
            word_count = Counter(words)
            term_frequency = word_count.get(search_term, 0)

            print(f"Frequency of '{search_term}' in document '{r['title']}': {term_frequency}")

            if results.has_matched_terms():
                print("Matched terms:", results.matched_terms())
    else:
        print(f"No results found for '{search_term}'")
