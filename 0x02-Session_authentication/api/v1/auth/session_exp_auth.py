#!/usr/bin/env python3
"""
Defines the SessionExpAuth class that extends SessionAuth
to include session expiration functionality.
"""
import os
from datetime import (
    datetime,
    timedelta
)

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Extends the SessionAuth class by adding support for session expiration
    based on a configurable duration.
    """
    def __init__(self):
        """
        Initialize the class and set the session expiration duration.
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Creates a session ID and associates it with the given user ID.
        Includes a timestamp indicating when the session was created.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Return:
            str: The generated session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID,
        ensuring the session is still valid based on its expiration.

        Args:
            session_id (str): The session ID to look up.

        Return:
            str: The associated user ID, or None if the session ID is invalid,
                 expired, or not found.
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")
