#!/usr/bin/env python3
"""Module providing routines for authentication tasks.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Encrypts a password using a secure hashing method.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Creates a new unique identifier.
    """
    return str(uuid4())


class Auth:
    """Handles authentication operations interacting with the database.
    """

    def __init__(self):
        """Sets up a new authentication instance with a database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the database.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user credentials during login.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Generates and assigns a session ID for a user.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if not user:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Finds a user based on their session ID.
        """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Removes the session ID linked to a user.
        """
        if user_id is not None:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Creates a password reset token for a user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Changes a user's password using a reset token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
