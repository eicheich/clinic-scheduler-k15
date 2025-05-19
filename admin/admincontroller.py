#!/usr/bin/env python
# Admin controller module for Clinic Scheduler System

# Importing required modules
import os
import sys

# Add parent directory to path to enable imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.login import logout

# Simple utility function
def display_header():
    # Show application header
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()
from auth.usermanager import add_user, update_user, delete_user, display_users
from schedule.schedulemanager import (
    add_schedule, get_all_schedules, update_schedule, delete_schedule, search_schedules,
    add_appointment, get_patient_appointments, update_appointment_status, get_appointment
)
from database import (
    get_appointments, get_schedules, get_appointment, get_user,
    add_appointment_db, update_appointment_db, delete_appointment_db
)

def add_doctor_schedule():
    # Add a new doctor schedule
    print("\n\n")
    display_header()
    print("ADD DOCTOR SCHEDULE")
    print("-" * 30)

    # Get doctor username
    display_users("Doctor")
    doctor_username = input("Enter doctor username: ")

    # Validate date format
    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        if len(date) != 10 or date[4] != '-' or date[7] != '-':
            print("Invalid date format. Use YYYY-MM-DD format (example: 2025-05-18)")
            continue
        try:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            if not (1 <= month <= 12 and 1 <= day <= 31):
                print("Invalid date. Month must be 1-12 and day must be 1-31.")
                continue
            break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD format (example: 2025-05-18)")

    # Validate time format
    while True:
        start_time = input("Enter start time (HH:MM): ")
        if len(start_time) != 5 or start_time[2] != ':':
            print("Invalid time format. Use HH:MM format (example: 08:00)")
            continue
        try:
            hour = int(start_time[0:2])
            minute = int(start_time[3:5])
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                print("Invalid time. Hour must be 0-23 and minute must be 0-59.")
                continue
            break
        except ValueError:
            print("Invalid time format. Use HH:MM format (example: 08:00)")

    while True:
        end_time = input("Enter end time (HH:MM): ")
        if len(end_time) != 5 or end_time[2] != ':':
            print("Invalid time format. Use HH:MM format (example: 12:00)")
            continue
        try:
            hour = int(end_time[0:2])
            minute = int(end_time[3:5])
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                print("Invalid time. Hour must be 0-23 and minute must be 0-59.")
                continue
            break
        except ValueError:
            print("Invalid time format. Use HH:MM format (example: 12:00)")

    # Validate end time is after start time
    start_hour, start_minute = int(start_time[0:2]), int(start_time[3:5])
    end_hour, end_minute = int(end_time[0:2]), int(end_time[3:5])
    if end_hour < start_hour or (end_hour == start_hour and end_minute <= start_minute):
        print("\nEnd time must be after start time.")
        input("Press Enter to return...")
        return

    # Save schedule to the database
    schedule_id = add_schedule(doctor_username, date, start_time, end_time)

    if schedule_id is not None:
        print(f"\nSchedule for doctor {doctor_username} on {date} ({start_time}-{end_time}) has been added successfully!")
    else:
        print(f"\nFailed to add schedule. Doctor username '{doctor_username}' might not be valid.")

    input("Press Enter to return...")

def view_doctor_schedules():
    # View all doctor schedules
    print("\n\n")
    display_header()
    print("DOCTOR SCHEDULES LIST")
    print("-" * 70)
    print(f"{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}{'STATUS':<10}")
    print("-" * 70)

    # Fetch all schedules from database
    schedules = get_all_schedules()

    if schedules:
        for schedule in schedules:
            doctor_name = schedule.get("doctor_name", "Unknown")
            specialization = schedule.get("specialization", "General")
            date = schedule.get("date", "")
            time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
            status = schedule.get("status", "Unknown")

            print(f"{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}{status:<10}")
    else:
        print("No doctor schedules available yet.")

    print("-" * 70)
    input("Press Enter to return...")

def update_doctor_schedule():
    # Update an existing doctor schedule
    print("\n\n")
    display_header()
    print("UPDATE DOCTOR SCHEDULE")
    print("-" * 30)

    # Get current date for comparison
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Show only future schedules or those for today
    print("Schedules available for update (upcoming schedules):")
    print("-" * 70)
    print(f"{'ID':<5}{'DOCTOR':<20}{'SPECIALIZATION':<20}{'DATE':<12}{'TIME':<15}{'STATUS':<10}")
    print("-" * 70)

    schedules = get_all_schedules()
    if not schedules:
        print("No doctor schedules to update.")
        input("Press Enter to return...")
        return

    # Filter for future schedules
    future_schedules = []
    for schedule in schedules:
        schedule_date = schedule.get("date", "")
        # Compare dates as strings (YYYY-MM-DD format ensures correct comparison)
        if schedule_date >= current_date:
            future_schedules.append(schedule)

    if not future_schedules:
        print("No upcoming schedules to update.")
        print("All schedules are in the past.")
        input("Press Enter to return...")
        return

    # Display future schedules for selection
    for schedule in future_schedules:
        schedule_id = schedule.get("id", "")
        doctor_name = schedule.get("doctor_name", "Unknown")
        specialization = schedule.get("specialization", "General")
        date = schedule.get("date", "")
        time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
        status = schedule.get("status", "Available")
        print(f"{schedule_id:<5}{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}{status:<10}")

    print("-" * 70)

    # Get schedule ID to update
    try:
        schedule_id = int(input("\nSelect schedule ID to update: "))

        # Find the selected schedule
        selected_schedule = None
        for schedule in future_schedules:
            if schedule.get("id") == schedule_id:
                selected_schedule = schedule
                break

        if not selected_schedule:
            print(f"\nID Schedule {schedule_id} not found.")
            input("Press Enter to return...")
            return

        # Get current values for reference
        current_doctor = selected_schedule.get("doctor_name", "Unknown")
        current_date = selected_schedule.get("date", "")
        current_start = selected_schedule.get("start_time", "")
        current_end = selected_schedule.get("end_time", "")
        current_status = selected_schedule.get("status", "Available")

        print(f"\nSchedule saat ini: {current_doctor} on {current_date} ({current_start}-{current_end})")
        print("Masukkan data baru (kosongkan jika tidak diubah):")

        # Get new values with validation
        # Date validation
        while True:
            date = input(f"Masukkan date baru (YYYY-MM-DD) [{current_date}]: ")
            if not date:  # Keep current value
                date = current_date
                break

            if len(date) != 10 or date[4] != '-' or date[7] != '-':
                print("Format date tidak valid. Gunakan format YYYY-MM-DD (contoh: 2025-05-18)")
                continue
            try:
                year = int(date[0:4])
                month = int(date[5:7])
                day = int(date[8:10])
                if not (1 <= month <= 12 and 1 <= day <= 31):
                    print("date tidak valid. Bulan harus 1-12 dan hari harus 1-31.")
                    continue
                break
            except ValueError:
                print("Format date tidak valid. Gunakan format YYYY-MM-DD (contoh: 2025-05-18)")

        # Start time validation
        while True:
            start_time = input(f"Masukkan waktu mulai baru (HH:MM) [{current_start}]: ")
            if not start_time:  # Keep current value
                start_time = current_start
                break

            if len(start_time) != 5 or start_time[2] != ':':
                print("Format waktu tidak valid. Gunakan format HH:MM (contoh: 08:00)")
                continue
            try:
                hour = int(start_time[0:2])
                minute = int(start_time[3:5])
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    print("Waktu tidak valid. Jam harus 0-23 dan menit harus 0-59.")
                    continue
                break
            except ValueError:
                print("Format waktu tidak valid. Gunakan format HH:MM (contoh: 08:00)")

        # End time validation
        while True:
            end_time = input(f"Masukkan waktu selesai baru (HH:MM) [{current_end}]: ")
            if not end_time:  # Keep current value
                end_time = current_end
                break

            if len(end_time) != 5 or end_time[2] != ':':
                print("Format waktu tidak valid. Gunakan format HH:MM (contoh: 12:00)")
                continue
            try:
                hour = int(end_time[0:2])
                minute = int(end_time[3:5])
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    print("Waktu tidak valid. Jam harus 0-23 dan menit harus 0-59.")
                    continue
                break
            except ValueError:
                print("Format waktu tidak valid. Gunakan format HH:MM (contoh: 12:00)")

        # Status options
        print("\nStatus Schedule:")
        print("1. Available (Tersedia)")
        print("2. Booked (Sudah Dipesan)")
        print("3. Cancelled (Dibatalkan)")

        status_choice = input(f"Pilih status (1-3) [{current_status}]: ")
        if status_choice == "1":
            status = "Available"
        elif status_choice == "2":
            status = "Booked"
        elif status_choice == "3":
            status = "Cancelled"
        elif not status_choice:  # Keep current value
            status = current_status
        else:
            print("Invalid choice, status tidak diubah.")
            status = current_status

        # Validate end time is after start time
        if start_time != current_start or end_time != current_end:
            start_hour, start_minute = int(start_time[0:2]), int(start_time[3:5])
            end_hour, end_minute = int(end_time[0:2]), int(end_time[3:5])
            if end_hour < start_hour or (end_hour == start_hour and end_minute <= start_minute):
                print("\nWaktu selesai harus setelah waktu mulai.")
                input("Press Enter to return...")
                return

        # Update the schedule in the database
        update_result = update_schedule(
            schedule_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            status=status
        )

        if update_result:
            print(f"\nSchedule ID {schedule_id} successfully diupdate!")
            print(f"Schedule baru: {current_doctor} on {date} ({start_time}-{end_time}), Status: {status}")
        else:
            print(f"\nFailed to mengupdate Schedule ID {schedule_id}. Please try again.")

    except ValueError:
        print("\nID Schedule harus berupa angka.")

    input("Press Enter to return...")

def delete_doctor_schedule():
    """Delete a doctor schedule."""
    print("\n\n")
    display_header()
    print("HAPUS Schedule DOKTER")
    print("-" * 30)

    # Get current date for comparison
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Show only future schedules or those for today
    print("Schedule yang tersedia untuk dihapus (Schedule yang belum dilaksanakan):")
    print("-" * 70)
    print(f"{'ID':<5}{'DOKTER':<20}{'SPECIALIZATION':<20}{'date':<12}{'WAKTU':<15}{'STATUS':<10}")
    print("-" * 70)

    schedules = get_all_schedules()
    if not schedules:
        print("Tidak ada Schedule dokter untuk dihapus.")
        input("Press Enter to return...")
        return

    # Filter for future schedules
    future_schedules = []
    for schedule in schedules:
        schedule_date = schedule.get("date", "")
        # Compare dates as strings (YYYY-MM-DD format ensures correct comparison)
        if schedule_date >= current_date:
            future_schedules.append(schedule)

    if not future_schedules:
        print("Tidak ada Schedule yang akan datang untuk dihapus.")
        print("Semua Schedule sudah lewat datenya.")
        input("Press Enter to return...")
        return

    # Display future schedules for selection
    for schedule in future_schedules:
        schedule_id = schedule.get("id", "")
        doctor_name = schedule.get("doctor_name", "Unknown")
        specialization = schedule.get("specialization", "General")
        date = schedule.get("date", "")
        time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
        status = schedule.get("status", "Available")

        print(f"{schedule_id:<5}{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}{status:<10}")

    print("-" * 70)    # Get schedule ID to delete
    try:
        schedule_id = int(input("\nPilih ID Schedule yang ingin dihapus: "))

        # Find the selected schedule
        selected_schedule = None
        for schedule in future_schedules:
            if schedule.get("id") == schedule_id:
                selected_schedule = schedule
                break

        if not selected_schedule:
            print(f"\nSchedule ID {schedule_id} not found.")
            input("Press Enter to return...")
            return

        # Get information for confirmation
        doctor_name = selected_schedule.get("doctor_name", "Unknown")
        date = selected_schedule.get("date", "")
        time_slot = f"{selected_schedule.get('start_time', '')}-{selected_schedule.get('end_time', '')}"

        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete the schedule for {doctor_name} on {date} ({time_slot})? (y/n): ")

        if confirm.lower() == 'y':
            # Delete the schedule
            delete_result = delete_schedule(schedule_id)

            if delete_result:
                print(f"\nSchedule ID {schedule_id} for {doctor_name} on {date} has been successfully deleted!")
            else:
                print(f"\nFailed to delete schedule ID {schedule_id}. Please try again.")
        else:
            print("\nDeletion cancelled.")

    except ValueError:
        print("\nID Schedule harus berupa angka.")

    input("Press Enter to return...")

def search_doctor_schedule():
    """Search for doctor schedules."""
    print("\n\n")
    display_header()
    print("CARI Schedule DOKTER")
    print("-" * 30)

    print("Pilih kriteria pencarian:")
    print("1. Nama dokter")
    print("2. date (YYYY-MM-DD)")
    print("3. Spesialisasi")

    choice = input("Pilih kriteria (1-3): ")

    search_results = []

    if choice == '1':
        doctor_name = input("Masukkan nama dokter: ")
        search_results = search_schedules(doctor_name=doctor_name)
    elif choice == '2':
        date = input("Masukkan date (YYYY-MM-DD): ")
        search_results = search_schedules(date=date)
    elif choice == '3':
        specialization = input("Masukkan spesialisasi: ")
        search_results = search_schedules(specialization=specialization)
    else:
        print("Invalid choice.")
        input("Press Enter to return...")
        return

    print("\nHasil pencarian:")
    print("-" * 70)
    print(f"{'ID':<5}{'DOKTER':<20}{'SPECIALIZATION':<20}{'date':<12}{'WAKTU':<15}")
    print("-" * 70)

    if search_results:
        for schedule in search_results:
            schedule_id = schedule.get("id", "")
            doctor_name = schedule.get("doctor_name", "Unknown")
            specialization = schedule.get("specialization", "General")
            date = schedule.get("date", "")
            time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"

            print(f"{schedule_id:<5}{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}")
    else:
        print("Tidak ada Schedule yang sesuai dengan kriteria pencarian.")

    print("-" * 70)
    input("Press Enter to return...")

def view_patient_queue():
    """View patient queues for all doctors."""
    print("\n\n")
    display_header()
    print("DAFTAR ANTRIAN PASIEN")
    print("-" * 80)
    print(f"{'DOKTER':<20}{'PASIEN':<20}{'date':<12}{'WAKTU':<15}{'NO ANTRIAN':<10}{'STATUS':<15}")
    print("-" * 80)

    # Get all schedules and appointments
    appointments = []

    # Import all appointment-related functions
    from database import get_appointments, get_schedules

    all_appointments = get_appointments()
    all_schedules = get_schedules()

    if all_appointments:
        for appointment in all_appointments:
            # Find the associated schedule
            schedule = None
            schedule_id = appointment.get("schedule_id")

            for s in all_schedules:
                if s.get("id") == schedule_id:
                    schedule = s
                    break

            if schedule:
                doctor_name = schedule.get("doctor_name", "Unknown")
                date = schedule.get("date", "")
                time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
                patient_name = appointment.get("patient_name", "Unknown")
                queue_number = appointment.get("queue_number", "")
                status = appointment.get("status", "Unknown")

                print(f"{doctor_name:<20}{patient_name:<20}{date:<12}{time_slot:<15}{queue_number:<10}{status:<15}")
    else:
        print("Belum ada antrian pasien.")

    print("-" * 80)
    input("Press Enter to return...")

def add_patient_appointment():
    """Add a new appointment for a patient (by admin)."""
    print("\n\n")
    display_header()
    print("TAMBAH appointment PASIEN")
    print("-" * 30)    # Step 1: Show available patients
    display_users("Patient")
    patient_username = input("Masukkan username pasien: ")

    # Verify patient exists
    patient_data = get_user(patient_username)
    if not patient_data or patient_data["role"] != "Patient":
        print(f"Error: Patient dengan username {patient_username} not found.")
        input("Press Enter to return...")
        return

    # Step 2: Show available schedules
    print("\n\n")
    display_header()
    print(f"TAMBAH appointment UNTUK PASIEN: {patient_data['name']}")
    print("-" * 70)
    print(f"{'ID':<5}{'DOKTER':<20}{'SPECIALIZATION':<20}{'date':<12}{'WAKTU':<15}{'STATUS':<10}")
    print("-" * 70)

    # Get all schedules
    schedules = get_all_schedules()
    available_schedules = []

    # Filter for available schedules
    for schedule in schedules:
        if schedule.get("status") == "Available":
            available_schedules.append(schedule)
            schedule_id = schedule.get("id", "")
            doctor_name = schedule.get("doctor_name", "Unknown")
            specialization = schedule.get("specialization", "General")
            date = schedule.get("date", "")
            time_slot = f"{schedule.get('start_time', '')}-{schedule.get('end_time', '')}"
            status = schedule.get("status", "")

            print(f"{schedule_id:<5}{doctor_name:<20}{specialization:<20}{date:<12}{time_slot:<15}{status:<10}")

    print("-" * 70)

    if not available_schedules:
        print("Tidak ada Schedule dokter yang tersedia.")
        input("Press Enter to return...")
        return

    # Step 3: Select schedule
    try:
        schedule_id = int(input("\nMasukkan ID Schedule: "))

        # Validate schedule
        selected_schedule = None
        for schedule in available_schedules:
            if schedule.get("id") == schedule_id:
                selected_schedule = schedule
                break

        if not selected_schedule:
            print("ID Schedule tidak valid atau Schedule tidak tersedia.")
            input("Press Enter to return...")
            return

        # Create the appointment
        doctor_name = selected_schedule.get("doctor_name", "Unknown")
        date = selected_schedule.get("date", "")

        # Add to database
        queue_number = add_appointment(schedule_id, patient_username)

        if queue_number > 0:
            print(f"\nsuccessfully membuat appointment untuk {patient_data['name']} dengan {doctor_name} on date {date}!")
            print(f"Nomor antrian: {queue_number}")

            # Update schedule status if needed
            # Check if admin wants to mark schedule as booked
            mark_booked = input("\nApakah Schedule ini akan ditandai sebagai 'Booked'? (y/n): ")
            if mark_booked.lower() == 'y':
                update_schedule(schedule_id, status="Booked")
                print("Status Schedule diupdate menjadi 'Booked'")
        else:
            print("\nFailed to membuat appointment. Please try again.")
    except ValueError:
        print("\nID Schedule harus berupa angka.")

    input("Press Enter to return...")

def update_patient_appointment():
    """Update an existing appointment."""
    print("\n\n")
    display_header()
    print("UPDATE appointment PASIEN")
    print("-" * 30)

    # Step 1: Display all appointments
    all_appointments = get_appointments()
    schedules = get_schedules()

    print("DAFTAR appointment:")
    print("-" * 80)
    print(f"{'ID':<5}{'PASIEN':<20}{'DOKTER':<20}{'date':<12}{'STATUS':<15}")
    print("-" * 80)

    if not all_appointments:
        print("Tidak ada appointment yang tersedia.")
        input("Press Enter to return...")
        return

    # Display appointments with schedule details
    for appointment in all_appointments:
        appointment_id = appointment.get("id", "")
        patient_name = appointment.get("patient_name", "Unknown")
        status = appointment.get("status", "Unknown")

        # Find associated schedule
        schedule_id = appointment.get("schedule_id")
        schedule_info = "Schedule not found"
        doctor_name = "Unknown"
        date = "Unknown"

        for schedule in schedules:
            if schedule.get("id") == schedule_id:
                doctor_name = schedule.get("doctor_name", "Unknown")
                date = schedule.get("date", "Unknown")
                break

        print(f"{appointment_id:<5}{patient_name:<20}{doctor_name:<20}{date:<12}{status:<15}")

    print("-" * 80)

    # Step 2: Select appointment to update
    try:
        appointment_id = int(input("\nMasukkan ID appointment yang akan diupdate: "))

        # Get appointment
        appointment = get_appointment(appointment_id)
        if not appointment:
            print(f"appointment dengan ID {appointment_id} not found.")
            input("Press Enter to return...")
            return

        # Display current status
        current_status = appointment.get("status", "Unknown")
        print(f"\nStatus saat ini: {current_status}")

        # Update status
        print("\nPilih status baru:")
        print("1. Menunggu (Waiting)")
        print("2. Sedang Diproses (In Progress)")
        print("3. Selesai (Completed)")
        print("4. Dibatalkan (Cancelled)")

        status_choice = input("Pilih status (1-4): ")

        if status_choice in ['1', '2', '3', '4']:
            statuses = ["Waiting", "In Progress", "Completed", "Cancelled"]
            new_status = statuses[int(status_choice) - 1]

            # Update in database
            if update_appointment_status(appointment_id, new_status):
                print(f"\nStatus appointment successfully diubah menjadi {new_status}!")
            else:
                print("\nFailed to mengupdate status appointment.")
        else:
            print("\nInvalid choice.")
    except ValueError:
        print("\nID appointment harus berupa angka.")

    input("Press Enter to return...")

def delete_patient_appointment():
    """Delete an existing appointment."""
    print("\n\n")
    display_header()
    print("HAPUS appointment PASIEN")
    print("-" * 30)

    # Step 1: Display all appointments
    all_appointments = get_appointments()
    schedules = get_schedules()

    print("DAFTAR appointment:")
    print("-" * 80)
    print(f"{'ID':<5}{'PASIEN':<20}{'DOKTER':<20}{'date':<12}{'STATUS':<15}")
    print("-" * 80)

    if not all_appointments:
        print("Tidak ada appointment yang tersedia.")
        input("Press Enter to return...")
        return

    # Display appointments with schedule details
    for appointment in all_appointments:
        appointment_id = appointment.get("id", "")
        patient_name = appointment.get("patient_name", "Unknown")
        status = appointment.get("status", "Unknown")

        # Find associated schedule
        schedule_id = appointment.get("schedule_id")
        schedule_info = "Schedule not found"
        doctor_name = "Unknown"
        date = "Unknown"

        for schedule in schedules:
            if schedule.get("id") == schedule_id:
                doctor_name = schedule.get("doctor_name", "Unknown")
                date = schedule.get("date", "Unknown")
                break

        print(f"{appointment_id:<5}{patient_name:<20}{doctor_name:<20}{date:<12}{status:<15}")

    print("-" * 80)

    # Step 2: Select appointment to delete
    try:
        appointment_id = int(input("\nMasukkan ID appointment yang akan dihapus: "))

        # Get appointment
        appointment = get_appointment(appointment_id)
        if not appointment:
            print(f"appointment dengan ID {appointment_id} not found.")
            input("Press Enter to return...")
            return

        # Get schedule and patient info for confirmation
        schedule_id = appointment.get("schedule_id")
        patient_name = appointment.get("patient_name", "Unknown")

        schedule_info = "Schedule not found"
        doctor_name = "Unknown"
        date = "Unknown"

        for schedule in schedules:
            if schedule.get("id") == schedule_id:
                doctor_name = schedule.get("doctor_name", "Unknown")
                date = schedule.get("date", "Unknown")
                break

        # Confirm deletion
        print(f"\nAnda akan menghapus appointment:")
        print(f"Pasien: {patient_name}")
        print(f"Dokter: {doctor_name}")
        print(f"date: {date}")

        confirm = input("\nLanjutkan penghapusan? (y/n): ")

        if confirm.lower() == 'y':
            # Delete from database
            if delete_appointment_db(appointment_id):
                print("\nappointment successfully dihapus!")

                # Ask if the schedule should be set back to Available
                reset_schedule = input("\nApakah Schedule dokter akan dikembalikan menjadi 'Available'? (y/n): ")
                if reset_schedule.lower() == 'y':
                    update_schedule(schedule_id, status="Available")
                    print("Status Schedule diupdate menjadi 'Available'")
            else:
                print("\nFailed to menghapus appointment.")
        else:
            print("\nPenghapusan dibatalkan.")
    except ValueError:
        print("\nID appointment harus berupa angka.")

    input("Press Enter to return...")

def display_appointment_menu():
    # Display and handle the appointment management menu
    while True:
        print("\n\n")
        display_header()
        print("APPOINTMENT MANAGEMENT MENU")
        print("-" * 30)
        print("1. View All Appointments")
        print("2. Add New Appointment")
        print("3. Update Appointment Status")
        print("4. Delete Appointment")
        print("5. Back to Admin Menu")
        print()

        choice = input("Choose menu (1-5): ")

        if choice == '1':
            view_patient_queue()
        elif choice == '2':
            add_patient_appointment()
        elif choice == '3':
            update_patient_appointment()
        elif choice == '4':
            delete_patient_appointment()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
            input("Press Enter to return...")

def display_admin_menu(admin_username):
    # Display and handle the admin menu functionality
    # admin_username: Admin number of the logged-in admin
    while True:
        print("\n\n")
        display_header()
        print("ADMIN MENU")
        print("-" * 30)
        print("1. Add Doctor Schedule (Create)")
        print("2. View Doctor Schedules (Read)")
        print("3. Update Doctor Schedule (Update)")
        print("4. Delete Doctor Schedule (Delete)")
        print("5. Search Doctor Schedules (Search)")
        print("6. Manage Appointments")
        print("7. Manage Users")
        print("8. Logout")
        print()

        choice = input("Choose menu (1-8): ")

        if choice == '1':
            add_doctor_schedule()
        elif choice == '2':
            view_doctor_schedules()
        elif choice == '3':
            update_doctor_schedule()
        elif choice == '4':
            delete_doctor_schedule()
        elif choice == '5':
            search_doctor_schedule()
        elif choice == '6':
            display_appointment_menu()
        elif choice == '7':
            display_user_management_menu()
        elif choice == '8':
            logout()
            break
        else:
            print("Invalid choice.")
            input("Press Enter to return...")

def display_user_management_menu():
    """Display and handle the user management menu."""
    while True:
        print("\n\n")
        display_header()
        print("MENU KELOLA PENGGUNA")
        print("-" * 30)
        print("1. View User List")
        print("2. Add New User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Back to Admin Menu")
        print()

        choice = input("Choose menu (1-5): ")

        if choice == '1':
            display_users()
        elif choice == '2':
            print("\n\n")
            display_header()
            print("ADD NEW USER")
            print("-" * 30)

            username = input("Username: ")
            password = input("Password: ")
            name = input("Full Name: ")

            print("\nChoose Role:")
            print("1. Admin")
            print("2. Doctor")
            print("3. Patient")
            role_choice = input("Choose role (1-3): ")

            if role_choice == '1':
                add_user(username, password, name, "Admin")
            elif role_choice == '2':
                specialization = input("Specialization: ")
                add_user(username, password, name, "Doctor", specialization=specialization)
            elif role_choice == '3':
                medical_record = input("Medical Record Number (optional): ")
                if medical_record:
                    add_user(username, password, name, "Patient", medical_record=medical_record)
                else:
                    add_user(username, password, name, "Patient")
            else:
                print("Invalid choice.")
                input("Press Enter to return...")
        elif choice == '3':
            username = input("Enter username to update: ")
            new_name = input("New name (leave empty if not changed): ")
            new_password = input("New password (leave empty if not changed): ")

            updates = {}
            if new_name:
                updates["name"] = new_name
            if new_password:
                updates["password"] = new_password

            update_user(username, **updates)
        elif choice == '4':
            username = input("Enter username to delete: ")
            confirm = input(f"Are you sure you want to delete user {username}? (y/n): ")

            if confirm.lower() == 'y':
                delete_user(username)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")
            input("Press Enter to return...")
