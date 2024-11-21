#!/usr/bin/env python3
"""A simple Flask app with a single route that returns a JSON payload.
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Handles GET requests to the root URL and returns a JSON payload."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
