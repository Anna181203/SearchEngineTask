import requests
from bs4 import BeautifulSoup
import re


prefix = 'https://www.ikw.uni-osnabrueck.de/en/'

start_url = prefix+'home.html'

agenda = [start_url]
visited = set()
index = {}

def build_index(text, url):
    """Build an in-memory index for the words in the page text."""
    words = re.findall(r'\w+', text.lower())  # Extract words
    for word in set(words):  # Avoid duplicate words
        if word not in index:
            index[word] = []
        index[word].append(url)

while agenda:
    url = agenda.pop()
    print("Get ",url)
    r = requests.get(url)
    print(r, r.encoding)
    if r.status_code == 200:
        print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.find_all('a'))

        visited.add(url)

        for link in soup.find_all('a', href=True):
            href = link['href']

            if href.startswith('http'):
                absolute_url = href
            elif href.startswith('/'):
                absolute_url = prefix + href[1:]
            else:
                absolute_url = url + href

            if absolute_url.startswith(prefix) and absolute_url not in visited:
                agenda.append(absolute_url)
    else:
        print(f"Failed to retrieve {url} with status code {r.status_code}")
        