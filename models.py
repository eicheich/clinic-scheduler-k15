import json
import os

class Schedule:
    def __init__(self, date, time, booked=False, patient_username=None):
        self.date = date
        self.time = time
        self.booked = booked
        self.patient_username = patient_username

    def to_dict(self):
        return {
            "date": self.date,
            "time": self.time,
            "booked": self.booked,
            "patient_username": self.patient_username
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['date'],
            data['time'],
            data.get('booked', False),
            data.get('patient_username')
        )

class Doctor:
    def __init__(self, name, specialty, schedule=None):
        self.name = name
        self.specialty = specialty
        self.schedule = schedule if schedule else []

    def to_dict(self):
        return {
            "name": self.name,
            "specialty": self.specialty,
            "schedule": [s.to_dict() for s in self.schedule]
        }

    @classmethod
    def from_dict(cls, data):
        schedule = [Schedule.from_dict(s) for s in data.get('schedule', [])]
        return cls(data['name'], data['specialty'], schedule)

class Patient:
    def __init__(self, username, name, bookings=None):
        self.username = username
        self.name = name
        self.bookings = bookings if bookings else []  # riwayat booking

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "bookings": self.bookings  # daftar jadwal yg sudah dibooking
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['username'],
            data['name'],
            data.get('bookings', [])
        )

# Fungsi database dasar
class Database:
    def __init__(self, path="data.json"):
        self.path = path
        self.doctors = []
        self.patients = []
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                data = json.load(f)
                self.doctors = [Doctor.from_dict(d) for d in data.get("doctors", [])]
                self.patients = [Patient.from_dict(p) for p in data.get("patients", [])]

    def save(self):
        with open(self.path, 'w') as f:
            json.dump({
                "doctors": [d.to_dict() for d in self.doctors],
                "patients": [p.to_dict() for p in self.patients]
            }, f, indent=2)
