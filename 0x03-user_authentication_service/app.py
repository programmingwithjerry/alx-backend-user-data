#!/usr/bin/env python3
"""A simple Flask app with a single route that returns a JSON payload.
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Handles GET requests to the root URL and returns a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Handles POST requests to /users for account creation.
    Returns:
        - A JSON response indicating the result of the operation.
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
