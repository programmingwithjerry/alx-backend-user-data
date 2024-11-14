#!/usr/bin/env python3
""" Blueprint setup for API routes
"""

# Importing necessary modules first
from flask import Blueprint


# Create a Blueprint named 'app_views' with the base URL prefix '/api/v1'
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


# Importing route handlers for index and users
from api.v1.views.index import *
from api.v1.views.users import *


# Load user data from file on initialization
User.load_from_file()
