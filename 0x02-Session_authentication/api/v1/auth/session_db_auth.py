#!/usr/bin/env python3
"""
Defines the SessionDBAuth class, which integrates session storage
into a database.
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Extends the SessionExpAuth class to enable storing and managing
    session data in a database.
    """

    def create_session(self, user_id=None):
        """
        Generates a session ID for the specified user ID and saves the
        session information to the database.

        Args:
           user_id (str): The ID of the user for whom the session is created.

        Return:
            str: The generated session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID by
        querying the database.

        Args:
            session_id (str): The session ID to look up.

        Return:
            str: The associated user ID, or None if the session ID is invalid
                 or not found.
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        Deletes a session from the database based on the session ID
        provided in a request cookie.

        Args:
            request: The HTTP request object containing session details.

        Return:
            bool: True if the session is successfully deleted, False otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
