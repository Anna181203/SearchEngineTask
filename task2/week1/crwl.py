import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

prefix = 'https://www.ikw.uni-osnabrueck.de/en/'
start_url = prefix + 'home.html'

agenda = [start_url]
agenda_set = {start_url}  # Set to track URLs already in the agenda
visited = set()
index = {}


def build_index(text, urltocheck):
    """Build an in-memory index for the words in the page text."""
    words = re.findall(r'\w+', text.lower())  # Extract words
    for word in set(words):  # Avoid duplicate words
        if word not in index:
            index[word] = []
        if urltocheck not in index[word]:  # Avoid duplicate URLs
            index[word].append(urltocheck)


def search(words):
    """Search the index for pages containing all given words."""
    results = None
    for word in words:
        if word in index:
            if results is None:
                results = set(index[word])
            else:
                results &= set(index[word])  # Intersection of URLs
        else:
            return []  # If any word is not found, return empty list
    return list(results) if results else []


def normalize_url(base_url, link):
    """Normalize the link to absolute URL relative to the base URL."""
    # Combine base URL with relative URL if necessary
    return urljoin(base_url, link)


while agenda:
    url = agenda.pop()
    agenda_set.remove(url)  # Remove URL from agenda_set as it is now being processed
    print("Processing:", url)

    try:
        r = requests.get(url)
        if r.status_code == 200 and 'text/html' in r.headers.get('Content-Type', ''):
            soup = BeautifulSoup(r.content, 'html.parser')
            build_index(soup.get_text(), url)  # Build index from page text
            visited.add(url)

            # Find and process links
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = normalize_url(url, href)

                # Only add the URL if it's within the same domain and not visited yet
                if absolute_url.startswith(prefix) and absolute_url not in visited and absolute_url not in agenda_set:
                    agenda.append(absolute_url)
                    agenda_set.add(absolute_url)  # Track the URL in agenda_set
        else:
            print(f"Skipping non-HTML or failed page: {url}")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

# Test the crawler
print("\nIndex built:")
for word, urls in index.items():
    print(f"{word}: {urls}")

# Test the search function
test_words = ['research', 'faculty']  # Example search terms
print("\nSearch results for", test_words, ":", search(test_words))
