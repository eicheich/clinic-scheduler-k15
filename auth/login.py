#!/usr/bin/env python
# Authentication module for Clinic Scheduler System

# Importing required modules
import os
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Admin, Doctor, Patient
from database import get_users, get_user

# Simple utility function
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

def authenticate(role):
    # Authenticate a user based on role
    print("\n\n")
    display_header()
    print(f"LOGIN AS {role.upper()}")
    print("-" * 30)

    if role == "Doctor":
        print("Username format: D0001, D0002, etc (doctor number)")
    elif role == "Patient":
        print("Username format: P0001, P0002, etc (patient number)")
    elif role == "Admin":
        print("Username format: A0001, A0002, etc (admin number)")

    username = input("Username: ")
    password = input("Password: ")

    # Get user from database
    user_data = get_user(username)    # Check if user exists and credentials match
    if user_data and user_data["password"] == password and user_data["role"] == role:
        print(f"\nLogin as {role} successful!")
        input("Press Enter to continue...")
        return username  # Return the username after successful authentication
    else:
        print("\nLogin failed. Username or password is incorrect.")
        input("Press Enter to return...")
        return None

def logout():
    # Logout the current user
    print("Logout successful.")
    input("Press Enter to continue...")
