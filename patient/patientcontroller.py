# Patient controller module for Clinic Scheduler System

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.login import logout
from schedule.schedulemanager import get_all_schedules, get_patient_appointments, search_schedules

def display_header():
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

def view_doctor_schedules():
    print("\n\n")
    display_header()
    print("DOCTOR SCHEDULES")
    print("-" * 70)
    print(f"{'ID':<5}{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}")
    print("-" * 70)
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
    print("\n\n")
    display_header()
    print("SEARCH DOCTORS")
    print("-" * 30)
    print("1. By Name")
    print("2. By Specialization")
    choice = input("Choose search criteria (1-2): ")
    if choice == '1':
        name = input("Enter doctor name: ")
        results = search_schedules(doctor_name=name)
    elif choice == '2':
        specialization = input("Enter specialization: ")
        results = search_schedules(specialization=specialization)
    else:
        print("Invalid choice.")
        input("Press Enter to return...")
        return
    print("\nSearch Results:")
    print("-" * 70)
    print(f"{'ID':<5}{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}")
    print("-" * 70)
    if results:
        for schedule in results:
            schedule_id = schedule.get("id", "")
            doctor_name = schedule.get("doctor_name", "Unknown")
            specialization = schedule.get("specialization", "General")
            date = schedule.get("date", "")
            time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
            print(f"{schedule_id:<5}{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}")
    else:
        print("No matching doctor schedules found.")
    print("-" * 70)
    input("Press Enter to return...")

def view_my_appointments(patient_username):
    print("\n\n")
    display_header()
    print("MY APPOINTMENTS")
    print("-" * 70)
    print(f"{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}{'STATUS':<10}")
    print("-" * 70)
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
