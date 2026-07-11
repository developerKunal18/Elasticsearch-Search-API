from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch(
    "http://localhost:9200"
)

# ---------- Add Product ----------
@app.route(
    "/products",
    methods=["POST"]
)
def add_product():

    data = request.get_json()

    es.index(
        index="products",
        document=data
    )

    return jsonify({
        "message": "Indexed Successfully"
    })


# ---------- Search ----------
@app.route("/search")
def search():

    keyword = request.args.get(
        "q",
        ""
    )

    result = es.search(

        index="products",

        query={
            "match": {
                "name": keyword
            }
        }
    )

    products = [

        item["_source"]

        for item in result["hits"]["hits"]

    ]

    return jsonify(products)


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(debug=True)
