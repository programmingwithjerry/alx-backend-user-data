#!/usr/bin/env python3
"""
Password Encryption
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generate a salted hash for the given password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ 
    Verify if the provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
