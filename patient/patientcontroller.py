#!/usr/bin/env python
# Patient controller module for Clinic Scheduler System

# Importing required modules
import os
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.login import logout
from schedule.schedulemanager import get_all_schedules, add_appointment, get_patient_appointments, search_schedules

# Simple utility function
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

def view_doctor_schedules():
    # View all available doctor schedules
    print("\n\n")
    display_header()
    print("DOCTOR SCHEDULES")
    print("-" * 70)
    print(f"{'ID':<5}{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}")
    print("-" * 70)

    # Fetch all available schedules from the database
    schedules = get_all_schedules()

    if schedules:
        for schedule in schedules:
            if schedule.get("status", "") == "Available":
                schedule_id = schedule.get("id", "")
                doctor_name = schedule.get("doctor_name", "Unknown")
                specialization = schedule.get("specialization", "General")
                date = schedule.get("date", "")
                time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"

                print(f"{schedule_id:<5}{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}")
    else:
        print("No doctor schedules available yet.")

    print("-" * 70)
    input("Press Enter to return...")

def search_doctors():
    # Search for doctors by name or specialization
    print("\n\n")
    display_header()
    print("SEARCH DOCTORS")
    print("-" * 30)

    search_term = input("Enter doctor name or specialization: ")

    # Search in schedules
    search_results = search_schedules(doctor_name=search_term) + search_schedules(specialization=search_term)

    # Remove duplicates by creating a unique set of doctor_usernames
    doctor_usernames = set()
    unique_results = []

    for schedule in search_results:
        doctor_username = schedule.get("doctor_username", "")
        if doctor_username and doctor_username not in doctor_usernames:
            doctor_usernames.add(doctor_username)
            unique_results.append(schedule)

    print("\nSearch results:")
    print("-" * 50)
    print(f"{'NAME':<20}{'SPECIALIZATION':<20}")
    print("-" * 50)

    if unique_results:
        for result in unique_results:
            doctor_name = result.get("doctor_name", "Unknown")
            specialization = result.get("specialization", "General")
            print(f"{doctor_name:<20}{specialization:<20}")
    else:
        print("No results found.")

    print("-" * 50)
    input("Press Enter to return...")

def view_my_appointments(patient_username):
    # View all appointments for the logged-in patient
    # patient_username: Medical record number of the logged-in patient
    print("\n\n")
    display_header()
    print("MY APPOINTMENTS")
    print("-" * 70)
    print(f"{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}{'STATUS':<10}")
    print("-" * 70)

    # Fetch patient's appointments from the database
    appointments = get_patient_appointments(patient_username)

    if appointments:
        for appointment in appointments:
            doctor_name = appointment.get("doctor_name", "Unknown")
            specialization = appointment.get("specialization", "General")
            date = appointment.get("date", "")
            time_slot = f"{appointment.get('start_time', '')}-{appointment.get('end_time', '')}"
            status = appointment.get("status", "Unknown")

            print(f"{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}{status:<10}")
    else:
        print("No appointments yet.")

    print("-" * 70)
    input("Press Enter to return...")

def display_patient_menu(patient_username):
    # Display and handle the patient menu functionality
    # patient_username: Medical record number of the logged-in patient
    while True:
        print("\n\n")
        display_header()
        print("PATIENT MENU")
        print("-" * 30)
        print("1. View Doctor Schedules")
        print("2. Search Doctors")
        print("3. View My Appointments")
        print("4. Logout")
        print()

        choice = input("Choose menu (1-4): ")

        if choice == '1':
            view_doctor_schedules()
        elif choice == '2':
            search_doctors()
        elif choice == '3':
            view_my_appointments(patient_username)
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice.")
            input("Press Enter to return...")
