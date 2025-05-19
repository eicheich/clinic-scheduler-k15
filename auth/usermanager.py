#!/usr/bin/env python
# User manager module for Clinic Scheduler System

# Importing required modules
import os
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Admin, Doctor, Patient
from database import get_users, get_user, add_user_db, update_user_db, delete_user_db, save_data, USERS_DB

# Simple utility function to display the header
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

# Helper functions for generating user IDs
def generate_doctor_number(doctor_count):
    # Generate doctor number based on count
    return f"D{doctor_count + 1:04d}"

def generate_patient_number(patient_count):
    # Generate patient number based on count
    return f"P{patient_count + 1:04d}"

def generate_admin_number(admin_count):
    # Generate admin number based on count
    return str(admin_count + 1)

# This module handles user management operations like:
# - Adding new users
# - Updating user profiles
# - Deleting users
# - Searching users
def add_user(username, password, name, role, **kwargs):
    # Add a new user to the system
    # username: Username for the new user (optional for Doctor and Patient)
    # password: Password for the new user
    # name: Full name of the user
    # role: Role of the user (Admin, Doctor, Patient)
    # **kwargs: Additional attributes based on user role
    users = get_users()

    if role == "Admin":
        # Count existing admins to generate admin number
        admin_count = sum(1 for _, user_data in users.items() if user_data.get("role") == "Admin")
        # Generate admin number
        admin_number = generate_admin_number(admin_count)
        # Use provided username or generated admin number        username = username or admin_number
        user = {"password": password, "role": role, "name": name, "admin_number": admin_number}
    elif role == "Doctor":
        # Count existing doctors to generate doctor number
        doctor_count = sum(1 for _, user_data in users.items() if user_data.get("role") == "Doctor")
        # Generate doctor number
        doctor_number = generate_doctor_number(doctor_count)
        # Use doctor number as username
        username = doctor_number
        specialization = kwargs.get("specialization", "General")
        user = {"password": password, "role": role, "name": name, "specialization": specialization, "doctor_number": doctor_number}
    elif role == "Patient":
        # Count existing patients to generate patient number
        patient_count = sum(1 for _, user_data in users.items() if user_data.get("role") == "Patient")
        # Generate patient number
        patient_number = generate_patient_number(patient_count)
        # Use patient number as username
        username = patient_number
        user = {"password": password, "role": role, "name": name, "patient_number": patient_number}

    if add_user_db(username, user):
        print(f"\nUser {username} with role {role} has been added successfully!")
    else:
        print(f"\nFailed to add user {username}. Username might already exist.")
    input("Press Enter to continue...")

def update_user(username, **kwargs):
    # Update user information
    # username: Username of the user to update
    # **kwargs: Fields to update and their new values
    user = get_user(username)
    if user:
        if update_user_db(username, **kwargs):
            print(f"\nUser {username} data has been updated successfully!")
        else:
            print(f"\nFailed to update user {username}.")
    else:
        print(f"\nUser {username} not found.")

    input("Press Enter to continue...")

def delete_user(username):
    # Delete a user from the system
    # username: Username of the user to delete
    user = get_user(username)
    if user:
        if delete_user_db(username):
            print(f"\nUser {username} has been deleted successfully!")
        else:
            print(f"\nFailed to delete user {username}.")
    else:
        print(f"\nUser {username} not found.")

    input("Press Enter to continue...")

def search_user(criteria):
    # Search for users based on given criteria
    # criteria: Search criteria (e.g., {"role": "Doctor", "specialization": "Cardiology"})
    # Returns: List of matching users
    results = []
    users = get_users()

    for username, user in users.items():
        match = True
        for key, value in criteria.items():
            if key not in user or user[key] != value:
                match = False
                break

        if match:
            results.append((username, user))

    return results

def display_users(role=None):
    # Display all users or users with a specific role
    # role: Filter users by role (optional, None shows all)
    print("\n\n")
    display_header()

    users = get_users()

    if role:
        print(f"USER LIST ({role.upper()})")
    else:
        print("ALL USERS LIST")

    print("-" * 50)
    print(f"{'USERNAME':<15}{'NAME':<25}{'ROLE':<15}")
    print("-" * 50)

    for username, user in users.items():
        if role is None or user["role"] == role:
            print(f"{username:<15}{user['name']:<25}{user['role']:<15}")

    print("-" * 50)
    input("Press Enter to return...")
