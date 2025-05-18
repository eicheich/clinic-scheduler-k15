import json
import os

USER_DB_PATH = "data/users.json"

def load_users():
    """Load user data from JSON file"""
    if not os.path.exists(USER_DB_PATH):
        return {"users": []}
    
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    """Save user data to JSON file"""
    os.makedirs(os.path.dirname(USER_DB_PATH), exist_ok=True)
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=2)

def login():
    """Handle user login"""
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    users_data = load_users()
    
    for user in users_data["users"]:
        if user["username"] == username and user["password"] == password:
            print(f"\nLogin successful! Welcome {'Dr. ' + username if user['role'] == 'doctor' else username}")
            return user  # Return user data for session
            
    print("\nError: Invalid username or password")
    return None

def logout():
    """Handle user logout"""
    print("\nLogout successful. Goodbye!")
    return None
