from bs4 import BeautifulSoup
from whoosh.index import open_dir, create_in
from whoosh.fields import Schema, TEXT, ID
import requests
import os

class Crawler:
    def __init__(self, start_url, prefix, index_dir="indexdir"):
        self.start_url = start_url
        self.prefix = prefix
        self.agenda = [start_url]
        self.visited = set()

        # Define or open Whoosh index
        schema = Schema(
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            url=ID(stored=True, unique=True)
        )
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            self.index = create_in(index_dir, schema)
        else:
            self.index = open_dir(index_dir)

    def add_to_index(self, title, content, url):
        """Add crawled page to the Whoosh index."""
        writer = self.index.writer()
        writer.add_document(title=title, content=content, url=url)
        writer.commit()
        print(f"Indexed: {title} ({url})")  # Debug statement

    def crawl(self):
        """Crawl pages starting from the seed URL."""
        while self.agenda:
            url = self.agenda.pop(0)
            if url in self.visited:
                continue
            print(f"Crawling: {url}")
            try:
                response = requests.get(url, timeout=5)
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    continue  # Skip non-HTML content

                soup = BeautifulSoup(response.text, 'html.parser')
                self.visited.add(url)

                # Extract data
                title = soup.title.string if soup.title else "No Title"
                content = soup.get_text()
                self.add_to_index(title, content, url)

                # Find and queue new links
                for link in soup.find_all('a', href=True):
                    absolute_url = self.prefix + link['href']
                    if absolute_url.startswith(self.prefix) and absolute_url not in self.visited:
                        self.agenda.append(absolute_url)

            except Exception as e:
                print(f"Failed to crawl {url}: {e}")

if __name__ == "__main__":
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    prefix = "https://vm009.rz.uos.de/crawl/"
    crawler = Crawler(start_url, prefix)
    crawler.crawl()
    print("Crawling and indexing completed!")
