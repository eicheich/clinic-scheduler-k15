from .login import load_users, save_users

def display_user(user):
    """Format user display based on role"""
    if user["role"] == "doctor":
        return f"Dr. {user['username']} ({user['role']})"
    return f"{user['username']} ({user['role']})"

def update_user():
    """Update existing user data"""
    print("\n=== Update User ===")
    username = input("Enter username to update: ").strip()
    
    users_data = load_users()
    found = False
    
    for user in users_data["users"]:
        if user["username"] == username:
            found = True
            print(f"\nCurrent data for {display_user(user)}:")
            print(f"1. Username: {user['username']}")
            print(f"2. Password: {'*' * len(user['password'])}")
            print(f"3. Role: {user['role']}")
            
            field = input("\nEnter field number to update (1-3): ").strip()
            new_value = input("Enter new value: ").strip()
            
            if field == "1":
                user["username"] = new_value
            elif field == "2":
                user["password"] = new_value
            elif field == "3":
                user["role"] = new_value
            else:
                print("Error: Invalid field number")
                return
            
            save_users(users_data)
            print("User updated successfully!")
            break
    
    if not found:
        print("Error: User not found")

def delete_user():
    """Delete a user account"""
    print("\n=== Delete User ===")
    username = input("Enter username to delete: ").strip()
    
    users_data = load_users()
    updated_users = [u for u in users_data["users"] if u["username"] != username]
    
    if len(updated_users) == len(users_data["users"]):
        print("Error: User not found")
    else:
        users_data["users"] = updated_users
        save_users(users_data)
        print("User deleted successfully!")

def list_users():
    """Display all users"""
    print("\n=== User List ===")
    users_data = load_users()
    
    if not users_data["users"]:
        print("No users found")
        return
    
    for idx, user in enumerate(users_data["users"], 1):
        print(f"{idx}. {display_user(user)}")
