# User authentication

import json
import os

# Path for users.json in the same folder as auth_utils.py
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

# Ensure users.json exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    """Load users from the JSON file."""
    with open(USERS_FILE, "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            users = {}
    return users

def save_users(users):
    """Save users dictionary to the JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def login(username, password):
    """Return True if username/password match."""
    users = load_users()
    return username in users and users[username] == password

def register(username, password):
    """
    Register a new user.
    Returns True if registration successful.
    Returns False if username already exists.
    """
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True
