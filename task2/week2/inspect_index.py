from whoosh.index import open_dir

def inspect_index(index_dir="indexdir"):
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        print(f"Indexed {searcher.doc_count()} documents.")
        for doc in searcher.all_stored_fields():
            print(doc)

if __name__ == "__main__":
    inspect_index()
