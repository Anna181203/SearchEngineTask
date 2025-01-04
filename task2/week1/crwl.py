import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

prefix = 'https://www.ikw.uni-osnabrueck.de/en/'

start_url = prefix+'home.html'

agenda = [start_url]
visited = set()

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
            # Manuelle Umwandlung der relativen URL in eine absolute URL
            href = link['href']

            if href.startswith('http'):
                # Wenn die URL schon absolut ist, verwenden wir sie direkt
                absolute_url = href
            elif href.startswith('/'):
                # Wenn die URL mit einem Schrägstrich beginnt, ist es eine relative URL zum Root-Verzeichnis
                absolute_url = prefix + href[1:]
            else:
                # Ansonsten ist es eine relative URL, die an die aktuelle URL angehängt werden muss
                absolute_url = url + href

            if absolute_url.startswith(prefix) and absolute_url not in visited:
                agenda.append(absolute_url)
    else:
        print(f"Failed to retrieve {url} with status code {r.status_code}")
        