#!/usr/bin/env python3
""" Module for managing user sessions. """
from models.base import Base


class UserSession(Base):
    """
    Represents a user session, linking a user ID to a session ID.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance with user and session data.

        Args:
            *args (list): Positional arguments.
            **kwargs (dict): Keyword arguments containing user
            and session details.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
