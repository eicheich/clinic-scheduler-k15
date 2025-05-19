#!/usr/bin/env python
# Database manager module for Clinic Scheduler System

# Importing required modules
import os
import json
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define database file paths
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
USERS_DB = os.path.join(DB_DIR, "users.json")
SCHEDULES_DB = os.path.join(DB_DIR, "schedules.json")
APPOINTMENTS_DB = os.path.join(DB_DIR, "appointments.json")

def load_data(file_path):
    """Load data from a JSON file.

    Args:
        file_path (str): Path to the JSON file

    Returns:
        dict or list: The data loaded from the JSON file
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Remove any comment lines (starting with //)
            lines = content.split('\n')
            clean_lines = [line for line in lines if not line.strip().startswith('//')]
            clean_content = '\n'.join(clean_lines)
            return json.loads(clean_content)
    except FileNotFoundError:
        if "users" in file_path:
            return {}
        else:
            return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {file_path}: {e}")
        print("Returning empty data structure")
        if "users" in file_path:
            return {}
        else:
            return []

def save_data(data, file_path):
    """Save data to a JSON file.

    Args:
        data (dict or list): The data to save
        file_path (str): Path to the JSON file

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # First check if the file exists and has a comment header
        comment = ""
        try:
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                if first_line.startswith('//'):
                    comment = first_line + '\n'
        except (FileNotFoundError, IOError):
            pass

        # Now save the data with the comment if it existed
        with open(file_path, 'w') as file:
            if comment:
                file.write(comment)
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# User database functions
def get_users():
    """Get all users from the database.

    Returns:
        dict: Dictionary of users
    """
    return load_data(USERS_DB)

def get_user(username):
    """Get a specific user from the database.

    Args:
        username (str): The username of the user to get

    Returns:
        dict: User data if found, None otherwise
    """
    users = get_users()
    return users.get(username)

def add_user_db(username, user_data):
    """Add a new user to the database.

    Args:
        username (str): Username for the new user
        user_data (dict): User data to add

    Returns:
        bool: True if successful, False if user already exists
    """
    users = get_users()
    if username in users:
        return False

    users[username] = user_data
    return save_data(users, USERS_DB)

def update_user_db(username, **kwargs):
    """Update an existing user in the database.

    Args:
        username (str): Username of the user to update
        **kwargs: Fields to update and their new values

    Returns:
        bool: True if successful, False if user doesn't exist
    """
    users = get_users()
    if username not in users:
        return False

    for key, value in kwargs.items():
        if key in users[username]:
            users[username][key] = value

    return save_data(users, USERS_DB)

def delete_user_db(username):
    """Delete a user from the database.

    Args:
        username (str): Username of the user to delete

    Returns:
        bool: True if successful, False if user doesn't exist
    """
    users = get_users()
    if username not in users:
        return False

    del users[username]
    return save_data(users, USERS_DB)

# Schedule database functions
def get_schedules():
    """Get all schedules from the database.

    Returns:
        list: List of schedule dictionaries
    """
    return load_data(SCHEDULES_DB)

def get_schedule(schedule_id):
    """Get a specific schedule from the database.

    Args:
        schedule_id (int): ID of the schedule to get

    Returns:
        dict: Schedule data if found, None otherwise
    """
    schedules = get_schedules()
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            return schedule
    return None

def get_doctor_schedules_db(doctor_username):
    """Get all schedules for a specific doctor from the database.

    Args:
        doctor_username (str): Username of the doctor

    Returns:
        list: List of schedule dictionaries for the specified doctor
    """
    schedules = get_schedules()
    return [s for s in schedules if s["doctor_username"] == doctor_username]

def add_schedule_db(schedule_data):
    """Add a new schedule to the database.

    Args:
        schedule_data (dict): Schedule data to add

    Returns:
        int: ID of the newly created schedule
    """
    schedules = get_schedules()

    # Generate a new ID if not provided
    if "id" not in schedule_data:
        if schedules:
            schedule_data["id"] = max(s["id"] for s in schedules) + 1
        else:
            schedule_data["id"] = 1

    schedules.append(schedule_data)
    save_data(schedules, SCHEDULES_DB)
    return schedule_data["id"]

def update_schedule_db(schedule_id, **kwargs):
    """Update an existing schedule in the database.

    Args:
        schedule_id (int): ID of the schedule to update
        **kwargs: Fields to update and their new values

    Returns:
        bool: True if successful, False if schedule doesn't exist
    """
    schedules = get_schedules()
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            for key, value in kwargs.items():
                if key in schedule:
                    schedule[key] = value
            return save_data(schedules, SCHEDULES_DB)
    return False

def delete_schedule_db(schedule_id):
    """Delete a schedule from the database.

    Args:
        schedule_id (int): ID of the schedule to delete

    Returns:
        bool: True if successful, False if schedule doesn't exist
    """
    schedules = get_schedules()
    for i, schedule in enumerate(schedules):
        if schedule["id"] == schedule_id:
            schedules.pop(i)
            return save_data(schedules, SCHEDULES_DB)
    return False

def search_schedules_db(**kwargs):
    """Search for schedules in the database based on criteria.

    Args:
        **kwargs: Search criteria (e.g., doctor_name, date, specialization)

    Returns:
        list: List of matching schedule dictionaries
    """
    schedules = get_schedules()
    results = []

    for schedule in schedules:
        match = True
        for key, value in kwargs.items():
            if key in schedule:
                # Case-insensitive partial matching for string fields
                if isinstance(schedule[key], str) and isinstance(value, str):
                    if value.lower() not in schedule[key].lower():
                        match = False
                        break
                # Exact matching for non-string fields
                elif schedule[key] != value:
                    match = False
                    break

        if match:
            results.append(schedule)

    return results

# Appointment database functions
def get_appointments():
    """Get all appointments from the database.

    Returns:
        list: List of appointment dictionaries
    """
    return load_data(APPOINTMENTS_DB)

def get_appointment(appointment_id):
    """Get a specific appointment from the database.

    Args:
        appointment_id (int): ID of the appointment to get

    Returns:
        dict: Appointment data if found, None otherwise
    """
    appointments = get_appointments()
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return None

def get_schedule_appointments(schedule_id):
    """Get all appointments for a specific schedule from the database.

    Args:
        schedule_id (int): ID of the schedule

    Returns:
        list: List of appointment dictionaries for the specified schedule
    """
    appointments = get_appointments()
    return [a for a in appointments if a["schedule_id"] == schedule_id]

def get_patient_appointments_db(patient_username):
    """Get all appointments for a specific patient from the database.

    Args:
        patient_username (str): Username of the patient

    Returns:
        list: List of appointment dictionaries with schedule details
    """
    appointments = get_appointments()
    patient_appointments = [a for a in appointments if a["patient_username"] == patient_username]

    # Add schedule details to each appointment
    schedules = get_schedules()
    result = []

    for appointment in patient_appointments:
        # Find the associated schedule
        schedule = None
        for s in schedules:
            if s["id"] == appointment["schedule_id"]:
                schedule = s
                break

        if schedule:
            appointment_with_details = {
                **appointment,
                "doctor_name": schedule["doctor_name"],
                "specialization": schedule["specialization"],
                "date": schedule["date"],
                "start_time": schedule["start_time"],
                "end_time": schedule["end_time"]
            }
            result.append(appointment_with_details)

    return result

def get_doctor_appointments_db(doctor_username):
    """Get all appointments for a specific doctor from the database.

    Args:
        doctor_username (str): Username of the doctor

    Returns:
        list: List of appointment dictionaries for the specified doctor
    """
    schedules = get_doctor_schedules_db(doctor_username)
    schedule_ids = [s["id"] for s in schedules]

    appointments = get_appointments()
    doctor_appointments = [a for a in appointments if a["schedule_id"] in schedule_ids]

    # Add schedule details to each appointment
    result = []

    for appointment in doctor_appointments:
        # Find the associated schedule
        schedule = None
        for s in schedules:
            if s["id"] == appointment["schedule_id"]:
                schedule = s
                break

        if schedule:
            appointment_with_details = {
                **appointment,
                "date": schedule["date"],
                "start_time": schedule["start_time"],
                "end_time": schedule["end_time"]
            }
            result.append(appointment_with_details)

    return result

def add_appointment_db(appointment_data):
    """Add a new appointment to the database.

    Args:
        appointment_data (dict): Appointment data to add

    Returns:
        int: ID of the newly created appointment
    """
    appointments = get_appointments()

    # Generate a new ID if not provided
    if "id" not in appointment_data:
        if appointments:
            appointment_data["id"] = max(a["id"] for a in appointments) + 1
        else:
            appointment_data["id"] = 1

    # Generate a queue number if not provided
    if "queue_number" not in appointment_data:
        schedule_appointments = [a for a in appointments if a["schedule_id"] == appointment_data["schedule_id"]]
        appointment_data["queue_number"] = len(schedule_appointments) + 1

    appointments.append(appointment_data)
    save_data(appointments, APPOINTMENTS_DB)
    return appointment_data["id"]

def update_appointment_db(appointment_id, **kwargs):
    """Update an existing appointment in the database.

    Args:
        appointment_id (int): ID of the appointment to update
        **kwargs: Fields to update and their new values

    Returns:
        bool: True if successful, False if appointment doesn't exist
    """
    appointments = get_appointments()
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            for key, value in kwargs.items():
                if key in appointment:
                    appointment[key] = value
            return save_data(appointments, APPOINTMENTS_DB)
    return False

def delete_appointment_db(appointment_id):
    """Delete an appointment from the database.

    Args:
        appointment_id (int): ID of the appointment to delete

    Returns:
        bool: True if successful, False if appointment doesn't exist
    """
    appointments = get_appointments()
    for i, appointment in enumerate(appointments):
        if appointment["id"] == appointment_id:
            appointments.pop(i)
            return save_data(appointments, APPOINTMENTS_DB)
    return False
