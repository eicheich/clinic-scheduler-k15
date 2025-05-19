#!/usr/bin/env python
# Models for Clinic Scheduler System

class User:
    # Base user class for the system
    def __init__(self, username, password, name, role):
        self.username = username
        self.password = password
        self.name = name
        self.role = role

class Admin(User):
    # Admin user class with specialized permissions
    def __init__(self, admin_number, password, name):
        # Admin number is a simple sequential number (e.g., 1, 2, etc.)
        super().__init__(admin_number, password, name, "Admin")
        self.admin_number = admin_number

class Doctor(User):
    # Doctor class with specialized attributes
    def __init__(self, doctor_number, password, name, specialization):        # Doctor number (e.g., D0001) is used as the username
        super().__init__(doctor_number, password, name, "Doctor")
        self.doctor_number = doctor_number
        self.specialization = specialization
        self.schedule = []

class Patient(User):
    # Patient class with specialized attributes
    def __init__(self, medical_record_number, password, name):        # Medical record number (e.g., P0001) is used as the username
        super().__init__(medical_record_number, password, name, "Patient")
        self.medical_record_number = medical_record_number
        self.appointments = []

class Schedule:
    # Schedule class to manage doctor appointments
    def __init__(self, doctor, date, start_time, end_time, status="Available"):
        self.doctor = doctor
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

class Appointment:
    # Appointment class to manage patient bookings
    def __init__(self, schedule, patient, queue_number):
        self.schedule = schedule
        self.patient = patient
        self.queue_number = queue_number
        self.status = "Waiting"  # Waiting, In Progress, Completed, Cancelled
