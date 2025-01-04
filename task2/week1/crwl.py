import requests
from bs4 import BeautifulSoup


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
        