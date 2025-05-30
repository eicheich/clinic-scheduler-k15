#!/usr/bin/env python
# Clinic Scheduler - Main Application

# Import system modules
import os
import sys

# Utility function
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

# Import application modules
from auth.login import authenticate
from admin.admincontroller import display_admin_menu
from doctor.doctorcontroller import display_doctor_menu
from patient.patientcontroller import display_patient_menu

# Main login menu
def display_login_menu():
    print("\n\n")
    display_header()
    print("LOGIN MENU")
    print("-" * 30)
    print("1. Login as Admin")
    print("2. Login as Doctor")
    print("3. Login as Patient")
    print("4. Exit")
    print()

# Main function
def main():
    while True:
        display_login_menu()
        choice = input("Choose menu (1-4): ")

        if choice == '1':  # Admin
            admin_username = authenticate("Admin")
            if admin_username:
                display_admin_menu(admin_username)
        elif choice == '2':  # Doctor
            doctor_username = authenticate("Doctor")
            if doctor_username:
                display_doctor_menu(doctor_username)
        elif choice == '3':  # Patient
            patient_username = authenticate("Patient")
            if patient_username:
                display_patient_menu(patient_username)
        elif choice == '4':  # Exit
            print("\n\n")
            print("Terima kasih telah menggunakan Clinic Scheduler System.")
            print("Sampai jumpa kembali!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk kembali...")

if __name__ == "__main__":
    main()
