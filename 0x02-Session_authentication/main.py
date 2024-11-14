# main.py
import os
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth

def get_auth_class():
    """Determines which authentication class to use based on environment variable."""
    auth_type = os.getenv("AUTH_TYPE", "basic")
    if auth_type == "session":
        return SessionAuth()
    return Auth()

# Testing the switch
if __name__ == "__main__":
    auth_instance = get_auth_class()
    print(f"Using authentication class: {auth_instance.__class__.__name__}")
