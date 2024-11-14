#!/usr/bin/env python3
"""
SessionAuth
"""

import uuid
from api.v1.auth.auth import Auth

class SessionAuth(Auth):
    """Session-based Authentication class."""

    # Dictionary to map session IDs to user IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a given user_id.

        Args:
            user_id (str): The user ID to create a session for.

        Return:
            The session ID if successful, or None if
            the user_id is invalid.
        """
        # Check for valid user_id
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Map session ID to user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

