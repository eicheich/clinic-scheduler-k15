from models import Doctor, Schedule, DataManager
from utils import ScheduleUtils

class Admin:
    def __init__(self):
        self.data_manager = DataManager()
        self.schedule_utils = ScheduleUtils()

    def add_doctor(self):
        print("\n--- Add New Doctor ---")
        doctor_id = input("Enter doctor ID: ")
        name = input("Enter doctor name: ")
        specialty = input("Enter specialty: ")
        contact = input("Enter contact info: ")
        
        new_doctor = Doctor(doctor_id, name, specialty, contact)
        doctors_data = self.data_manager.load_data(self.data_manager.doctors_file)
        doctors_data["doctors"].append(new_doctor.to_dict())
        self.data_manager.save_data(self.data_manager.doctors_file, doctors_data)
        print("Doctor added successfully!")

    def add_schedule(self):
        print("\n--- Add Doctor Schedule ---")
        doctor_id = input("Enter doctor ID: ")
        date = input("Enter date (YYYY-MM-DD): ")
        start_time = input("Enter start time (HH:MM): ")
        end_time = input("Enter end time (HH:MM): ")
        
        time_slots = self.schedule_utils.create_time_slots(start_time, end_time)
        new_schedule = Schedule(doctor_id, date, time_slots)
        
        schedules_data = self.data_manager.load_data(self.data_manager.schedules_file)
        schedules_data["schedules"].append(new_schedule.to_dict())
        self.data_manager.save_data(self.data_manager.schedules_file, schedules_data)
        print("Schedule added successfully!")

class UserApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.schedule_utils = ScheduleUtils()

    def view_doctors(self):
        doctors = self.schedule_utils.get_available_doctors()
        print("\n--- Available Doctors ---")
        for doctor in doctors:
            print(f"ID: {doctor['id']}, Name: {doctor['name']}, Specialty: {doctor['specialty']}")

    def book_appointment(self):
        self.view_doctors()
        doctor_id = input("\nEnter doctor ID to book appointment: ")
        schedule = self.schedule_utils.get_doctor_schedule(doctor_id)
        
        if not schedule:
            print("No schedule found for this doctor.")
            return
        
        if not self.schedule_utils.filter_expired_slots(schedule):
            print("All slots for this date have expired.")
            return
        
        print(f"\nAvailable slots for {schedule['date']}:")
        available_slots = [slot for slot in schedule["time_slots"] if slot["available"]]
        for i, slot in enumerate(available_slots):
            print(f"{i+1}. {slot['time']}")
        
        if not available_slots:
            print("No available slots for this doctor.")
            return
        
        choice = int(input("Select slot number: ")) - 1
        if 0 <= choice < len(available_slots):
            selected_slot = available_slots[choice]
            selected_slot["available"] = False
            selected_slot["patient"] = "Patient Name"  # In real app, you'd get user info
            
            schedules_data = self.data_manager.load_data(self.data_manager.schedules_file)
            for s in schedules_data["schedules"]:
                if s["doctor_id"] == doctor_id and s["date"] == schedule["date"]:
                    s["time_slots"] = schedule["time_slots"]
                    break
            
            self.data_manager.save_data(self.data_manager.schedules_file, schedules_data)
            print(f"Appointment booked for {selected_slot['time']}!")
        else:
            print("Invalid slot selection.")

def main():
    print("Welcome to Doctor's Scheduling System")
    while True:
        print("\n1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        choice = input("Select option: ")
        
        if choice == "1":
            admin = Admin()
            while True:
                print("\nAdmin Menu:")
                print("1. Add Doctor")
                print("2. Add Schedule")
                print("3. Back to Main Menu")
                admin_choice = input("Select option: ")
                
                if admin_choice == "1":
                    admin.add_doctor()
                elif admin_choice == "2":
                    admin.add_schedule()
                elif admin_choice == "3":
                    break
                else:
                    print("Invalid choice.")
        
        elif choice == "2":
            user = UserApp()
            while True:
                print("\nUser Menu:")
                print("1. View Doctors")
                print("2. Book Appointment")
                print("3. Back to Main Menu")
                user_choice = input("Select option: ")
                
                if user_choice == "1":
                    user.view_doctors()
                elif user_choice == "2":
                    user.book_appointment()
                elif user_choice == "3":
                    break
                else:
                    print("Invalid choice.")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
