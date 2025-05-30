#!/usr/bin/env python
# Schedule manager module for Clinic Scheduler System

# Importing required modules
import os
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple utility function
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()
from database import (
    get_schedules, get_schedule, get_doctor_schedules_db,
    add_schedule_db, update_schedule_db, delete_schedule_db, search_schedules_db,
    get_appointments, get_appointment, get_schedule_appointments,
    get_patient_appointments_db, get_doctor_appointments_db,
    add_appointment_db, update_appointment_db, delete_appointment_db,
    get_user
)

def has_schedule_conflict(doctor_username, date, start_time, end_time, exclude_schedule_id=None):
    """
    Check if the doctor has a conflicting schedule on the same date and time range.
    Returns True if there is a conflict, False otherwise.
    exclude_schedule_id: If updating, exclude this schedule from the check.
    """
    from datetime import datetime
    schedules = get_doctor_schedules(doctor_username)
    new_start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    new_end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
    for schedule in schedules:
        if exclude_schedule_id and schedule.get("id") == exclude_schedule_id:
            continue
        if schedule.get("date") != date:
            continue
        existing_start = datetime.strptime(f"{schedule['date']} {schedule['start_time']}", "%Y-%m-%d %H:%M")
        existing_end = datetime.strptime(f"{schedule['date']} {schedule['end_time']}", "%Y-%m-%d %H:%M")
        # Check for overlap
        if new_start < existing_end and new_end > existing_start:
            return True
    return False

def add_schedule(doctor_username, date, start_time, end_time):
    # Add a new doctor schedule
    # doctor_username: Doctor number (D001, D002, etc.)
    # date: Date in YYYY-MM-DD format
    # start_time: Start time in HH:MM format
    # end_time: End time in HH:MM format
    # Returns ID of the newly created schedule
    # Get doctor info from the database
    doctor_data = get_user(doctor_username)

    if not doctor_data:
        print(f"Error: Doctor with username {doctor_username} not found")
        return None

    doctor_name = doctor_data.get("name", "Unknown Doctor")
    specialization = doctor_data.get("specialization", "General")

    new_schedule = {
        "doctor_username": doctor_username,
        "doctor_name": doctor_name,
        "specialization": specialization,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "status": "Available"
    }

    # Check for schedule conflict
    if has_schedule_conflict(doctor_username, date, start_time, end_time):
        print(f"Error: Schedule conflict detected for doctor {doctor_username} on {date} between {start_time}-{end_time}.")
        return None

    # Add the schedule to the database
    return add_schedule_db(new_schedule)

def get_all_schedules():
    # Get all doctor schedules
    # Returns list of all schedules
    return get_schedules()

def get_doctor_schedules(doctor_username):
    # Get schedules for a specific doctor
    # doctor_username: Doctor number (D001, D002, etc.)
    # Returns list of schedules for the specified doctor
    return get_doctor_schedules_db(doctor_username)

def update_schedule(schedule_id, **kwargs):
    # Update an existing schedule
    # schedule_id: ID of the schedule to update
    # **kwargs: Fields to update and their new values
    # If updating time/date, check for conflict
    schedule = get_schedule(schedule_id)
    if not schedule:
        return False
    doctor_username = schedule.get("doctor_username")
    date = kwargs.get("date", schedule.get("date"))
    start_time = kwargs.get("start_time", schedule.get("start_time"))
    end_time = kwargs.get("end_time", schedule.get("end_time"))
    if has_schedule_conflict(doctor_username, date, start_time, end_time, exclude_schedule_id=schedule_id):
        print(f"Error: Schedule conflict detected for doctor {doctor_username} on {date} between {start_time}-{end_time}.")
        return False
    return update_schedule_db(schedule_id, **kwargs)

def delete_schedule(schedule_id):
    # Delete a schedule
    # schedule_id: ID of the schedule to delete
    # Returns True if deleted successfully, False otherwise
    return delete_schedule_db(schedule_id)

def search_schedules(**kwargs):
    # Search for schedules based on criteria
    # **kwargs: Search criteria (e.g., doctor_name, date, specialization)
    # Returns list of matching schedules
    return search_schedules_db(**kwargs)

def add_appointment(schedule_id, patient_username):
    # Add a new appointment for a patient
    # schedule_id: ID of the schedule
    # patient_username: Medical record number of the patient (P001, P002, etc.)
    # Returns queue number for the appointment
    # Find the schedule
    schedule = get_schedule(schedule_id)
    if not schedule:
        return 0

    # Find existing appointments for this schedule
    existing_appointments = get_schedule_appointments(schedule_id)
    queue_number = len(existing_appointments) + 1

    # Get patient info from database
    patient_data = get_user(patient_username)
    if not patient_data:
        print(f"Error: Patient with username {patient_username} not found")
        return 0

    patient_name = patient_data.get("name", "Unknown Patient")

    # Create new appointment
    new_appointment = {
        "schedule_id": schedule_id,
        "patient_username": patient_username,
        "patient_name": patient_name,
        "queue_number": queue_number,
        "status": "Waiting"
    }

    # Add the appointment to the database
    appointment_id = add_appointment_db(new_appointment)
    if appointment_id:
        return queue_number
    return 0

def get_patient_appointments(patient_username):
    # Get all appointments for a specific patient
    # patient_username: Medical record number of the patient (P001, P002, etc.)
    # Returns list of appointments with schedule details
    return get_patient_appointments_db(patient_username)

def get_doctor_appointments(doctor_username):
    # Get all appointments for a specific doctor
    # doctor_username: Doctor number (D001, D002, etc.)
    # Returns list of appointments for the specified doctor
    return get_doctor_appointments_db(doctor_username)

def update_appointment_status(appointment_id, new_status):
    # Update the status of an appointment
    # appointment_id: ID of the appointment
    # new_status: New status value ('Waiting', 'In Progress', 'Completed', 'Cancelled')
    # Returns True if updated successfully, False otherwise
    valid_statuses = ["Waiting", "In Progress", "Completed", "Cancelled"]

    if new_status not in valid_statuses:
        return False

    return update_appointment_db(appointment_id, status=new_status)
