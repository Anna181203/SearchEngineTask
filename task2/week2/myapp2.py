from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

app = Flask(__name__)

# Open the Whoosh index
index_dir = "indexdir"
ix = open_dir(index_dir)


@app.route("/")
def home():
    """Render the search form."""
    return render_template('start.html')


@app.route("/search")
def search():
    """Handle the search query and display results."""
    query_string = request.args.get("q", "")
    results = []

    if query_string:
        # Query the Whoosh index
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(query_string)
            whoosh_results = searcher.search(query)

            # Collect results
            for result in whoosh_results:
                results.append({
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result.highlights("content")
                })

    return render_template('results.html', query=query_string, results=results)


if __name__ == "__main__":
    app.run(debug=True)

