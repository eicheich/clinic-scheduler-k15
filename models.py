# Models for Clinic Scheduler System

class User:
    def __init__(self, username, password, name, role):
        self.username = username
        self.password = password
        self.name = name
        self.role = role

class Admin(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, name, "Admin")

class Doctor(User):
    def __init__(self, username, password, name, specialization="General"):
        super().__init__(username, password, name, "Doctor")
        self.specialization = specialization

class Patient(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, name, "Patient")

class Schedule:
    def __init__(self, id, doctor_name, specialization, date, start_time, end_time, status="Available"):
        self.id = id
        self.doctor_name = doctor_name
        self.specialization = specialization
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

class Appointment:
    def __init__(self, id, schedule_id, patient_name, queue_number, status="Waiting"):
        self.id = id
        self.schedule_id = schedule_id
        self.patient_name = patient_name
        self.queue_number = queue_number
        self.status = status
