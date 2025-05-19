#!/usr/bin/env python
# Doctor controller module for Clinic Scheduler System

# Importing required modules
import os
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.login import logout
from schedule.schedulemanager import get_doctor_schedules, get_doctor_appointments, update_appointment_status

# Simple utility function
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

def view_my_schedule(doctor_username):
    # Display schedule for the logged-in doctor
    print("\n\n")
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()
    print(f"MY SCHEDULE ({doctor_username})")
    print("-" * 50)
    print(f"{'DATE':<15}{'TIME':<20}{'STATUS':<15}")
    print("-" * 50)

    # Fetch doctor's schedules from the database
    schedules = get_doctor_schedules(doctor_username)

    if schedules:
        for schedule in schedules:
            date = schedule.get("date", "")
            time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
            status = schedule.get("status", "Unknown")

            print(f"{date:<15}{time_slot:<20}{status:<15}")
    else:
        print("No schedules available for you yet.")

    print("-" * 50)
    input("Press Enter to return...")

def view_my_patients(doctor_username):
    # Menampilkan antrian pasien untuk dokter yang sedang login
    print("\n\n")
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()
    print(f"ANTRIAN PASIEN SAYA ({doctor_username})")
    print("-" * 70)
    print(f"{'TANGGAL':<15}{'PASIEN':<20}{'NO ANTRIAN':<15}{'STATUS':<15}")
    print("-" * 70)

    # Fetch doctor's appointments from the database
    appointments = get_doctor_appointments(doctor_username)

    if appointments:
        for appointment in appointments:
            date = appointment.get("date", "")
            patient_name = appointment.get("patient_name", "Unknown")
            queue_number = appointment.get("queue_number", "")
            status = appointment.get("status", "Unknown")

            print(f"{date:<15}{patient_name:<20}{queue_number:<15}{status:<15}")
    else:
        print("Belum ada antrian pasien.")

    print("-" * 70)
    input("Tekan Enter untuk kembali...")

def display_doctor_menu(doctor_username):
    # Display and handle the doctor menu functionality
    # doctor_username: Doctor number of the logged-in doctor
    while True:
        print("\n\n")
        display_header()
        print("MENU DOKTER")
        print("-" * 30)
        print("1. Lihat Jadwal Saya")
        print("2. Lihat Antrian Pasien Saya")
        print("3. Update Status Pasien")
        print("4. Logout")
        print()

        choice = input("Pilih menu (1-4): ")

        if choice == '1':
            view_my_schedule(doctor_username)
        elif choice == '2':
            view_my_patients(doctor_username)
        elif choice == '3':
            update_patient_status(doctor_username)
        elif choice == '4':
            logout()
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk kembali...")

def update_patient_status(doctor_username="doctor1"):
    # Update the status of a patient in the queue
    # doctor_username: Username of the logged-in doctor
    print("\n\n")
    display_header()
    print("UPDATE STATUS PASIEN")
    print("-" * 30)

    # Get doctor's appointments
    appointments = get_doctor_appointments(doctor_username)

    if not appointments:
        print("Belum ada antrian pasien untuk Anda.")
        input("Tekan Enter untuk kembali...")
        return

    # Display current queue
    print(f"ANTRIAN PASIEN SAYA ({doctor_username})")
    print("-" * 70)
    print(f"{'ID':<5}{'TANGGAL':<15}{'PASIEN':<20}{'NO ANTRIAN':<15}{'STATUS':<15}")
    print("-" * 70)

    for appointment in appointments:
        appointment_id = appointment.get("id", "")
        date = appointment.get("date", "")
        patient_name = appointment.get("patient_name", "Unknown")
        queue_number = appointment.get("queue_number", "")
        status = appointment.get("status", "Unknown")

        print(f"{appointment_id:<5}{date:<15}{patient_name:<20}{queue_number:<15}{status:<15}")

    print("-" * 70)

    # Get appointment ID to update
    try:
        appointment_id = int(input("\nPilih ID antrian yang akan diupdate: "))

        # Verify appointment exists and belongs to this doctor
        selected_appointment = None
        for appointment in appointments:
            if appointment.get("id") == appointment_id:
                selected_appointment = appointment
                break

        if not selected_appointment:
            print(f"\nID antrian {appointment_id} tidak ditemukan.")
            input("Tekan Enter untuk kembali...")
            return

        # Get information for confirmation
        patient_name = selected_appointment.get("patient_name", "Unknown")
        current_status = selected_appointment.get("status", "Unknown")

        print(f"\nPasien: {patient_name}")
        print(f"Status saat ini: {current_status}")

        print("\nPilih status baru:")
        print("1. Sedang Diproses (In Progress)")
        print("2. Selesai (Completed)")
        print("3. Dibatalkan (Cancelled)")

        status_choice = input("Pilih status (1-3): ")

        if status_choice in ['1', '2', '3']:
            statuses = ["In Progress", "Completed", "Cancelled"]
            new_status = statuses[int(status_choice) - 1]

            # Update the appointment status
            update_result = update_appointment_status(appointment_id, new_status)

            if update_result:
                print(f"\nStatus antrian untuk {patient_name} berhasil diubah menjadi {new_status}!")
            else:
                print("\nGagal mengupdate status antrian.")
        else:
            print("\nPilihan tidak valid.")

    except ValueError:
        print("\nID antrian harus berupa angka.")

    input("Tekan Enter untuk kembali...")
