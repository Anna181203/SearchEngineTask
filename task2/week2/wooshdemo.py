from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID


# Here, the structure of index entires is defined. You can add more fields with metadata, computed values etc.,
# and use them for searching and ranking. 
# We only use a title and a text.
#
# The "stored" attribute is used for all parts that we want to be able to fully retrieve from the index
#
# schema = Schema(title=TEXT(stored=True), content=TEXT)

# Create an index in the directory indexdr (the directory must already exist!)
ix = create_in("indexdir", schema)
writer = ix.writer()

# write the index to the disk
writer.commit()

# Retrieving data
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    # find entries with the words 'first' AND 'last'
    query = QueryParser("content", ix.schema).parse("first last")
    results = searcher.search(query)

    # print all results
    for r in results:
        print(r)
        
