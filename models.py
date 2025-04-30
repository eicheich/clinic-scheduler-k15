import json
from datetime import datetime, timedelta
from pathlib import Path

class Doctor:
    def __init__(self, id, name, specialty, contact):
        self.id = id
        self.name = name
        self.specialty = specialty
        self.contact = contact

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "contact": self.contact
        }

class Schedule:
    def __init__(self, doctor_id, date, time_slots):
        self.doctor_id = doctor_id
        self.date = date
        self.time_slots = time_slots

    def to_dict(self):
        return {
            "doctor_id": self.doctor_id,
            "date": self.date,
            "time_slots": self.time_slots
        }

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.appointments = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "appointments": self.appointments
        }

class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.doctors_file = self.data_dir / "doctors.json"
        self.schedules_file = self.data_dir / "schedules.json"
        self.users_file = self.data_dir / "users.json"
        self.initialize_files()

    def initialize_files(self):
        if not self.doctors_file.exists():
            self.doctors_file.write_text('{"doctors": []}')
        if not self.schedules_file.exists():
            self.schedules_file.write_text('{"schedules": []}')
        if not self.users_file.exists():
            self.users_file.write_text('{"users": []}')

    def load_data(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def save_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
