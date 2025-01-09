from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os

def create_index(index_dir="indexdir"):
    """Creates or opens a Whoosh index."""
    schema = Schema(
        title=TEXT(stored=True),         # Title of the document
        content=TEXT(stored=True),      # Content of the document
        url=ID(stored=True, unique=True)  # URL field (stored and unique)
    )
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return create_in(index_dir, schema)
    else:
        from whoosh.index import open_dir
        return open_dir(index_dir)

if __name__ == "__main__":
    index_dir = "indexdir"
    create_index(index_dir)
    print(f"Index initialized at {index_dir}. Ready for population!")
