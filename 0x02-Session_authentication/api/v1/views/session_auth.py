#!/usr/bin/env python3

"""
Session-based Authentication Endpoints
"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Returns:
      - Response object with login result
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    # Check if email is provided, if missing return error
    if not user_email:
        return jsonify(error="email missing"), 400

    # Check if password is provided, if missing return error
    if not user_pwd:
        return jsonify(error="password missing"), 400

    try:
        # Attempt to find user by email
        user = User.search({"email": user_email})
    except Exception:
        return jsonify(error="no user found for this email"), 404

    # Check if user exists, if not found return error
    if not user:
        return jsonify(error="no user found for this email"), 404

    # Validate the password for each user found
    for u in user:
        if u.is_valid_password(user_pwd):
            user_id = u.id
            from api.v1.app import auth
            session_id = auth.create_session(user_id)

            # Create response with user data and set session cookie
            response = jsonify(u.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify(error="wrong password"), 401

    # If no matching user is found after loop, return error
    return jsonify(error="no user found for this email"), 404
