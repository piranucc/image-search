from flask import Flask, render_template, request, jsonify

import json
import os
import uuid
import ProcessImage

from elasticsearch import Elasticsearch

app = Flask(__name__, static_folder="static")


@app.route("/")
def api_root():
    return render_template("test.html")


@app.route("/upload_file", methods=["POST"])
def api_upload():
    if request.method != 'POST':
        return "no"

    upload = request.files['file']

    image_id = str(uuid.uuid4())
    upload.save(os.path.join(os.getcwd(), "static/uploads/") + image_id)

    url = ["http://localhost:5000/static/uploads/" + image_id]
    tags = ProcessImage.process_image(url)

    doc = {
        "image_name": image_id,
        "tags": tags
    }

    es = Elasticsearch()
    es.index(index="image-search", doc_type="image", id=image_id,
             body=json.dumps(doc))

    return jsonify({"message": "success"})

if __name__ == "__main__":
    app.run(debug=True)
