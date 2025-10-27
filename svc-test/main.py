from flask import Flask, request, jsonify
import json

from save import save

app = Flask(__name__)

@app.route("/dota2", methods=["POST"])
def process():
    content = request.json

    print(content)

    return jsonify(message={"state": "succeed"}, status=200), 200

if __name__ == "__main__":
    app.run()