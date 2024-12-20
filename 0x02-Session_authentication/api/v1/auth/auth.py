#!/usr/bin/env python3
"""
Module for API authentication
"""

from tabnanny import check
from flask import request
from typing import TypeVar, List
from os import getenv
User = TypeVar('User')


class Auth:
    """ Handles authentication methods """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is needed for
            specific API routes """
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('*') and path.startswith(i[:-1]):
                return False
            elif i in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Verifies the presence of the Authorization
            header in the request
        and checks if it contains a value """
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Placeholder method for obtaining the current user """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from the request.
        """
        if request:
            session_name = getenv("SESSION_NAME")
            if session_name:
                return request.cookies.get(session_name, None)
        return None
