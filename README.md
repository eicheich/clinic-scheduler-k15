# Clinic Scheduler System

A simple clinic scheduling system implemented in Python.

## Project Structure

```
clinic-scheduler-k15/
├── main.py                  # Main application entry point
├── models.py                # Data models
├── common.py                # Common utility functions
├── admin/                   # Admin module
│   ├── __init__.py
│   └── admincontroller.py   # Admin management functions
├── auth/                    # Authentication module
│   ├── __init__.py
│   ├── login.py             # Login and logout functions
│   └── usermanager.py       # User management operations
├── doctor/                  # Doctor module
│   ├── __init__.py
│   └── doctorcontroller.py  # Doctor-related functions
├── patient/                 # Patient module
│   ├── __init__.py
│   └── patientcontroller.py # Patient-related functions
├── schedule/                # Schedule module
│   ├── __init__.py
│   └── schedulemanager.py   # Schedule management functions
```

## Module Responsibilities

### auth/login.py
- Handles all login and logout functionality
- Authentication of users based on their roles

### auth/usermanager.py
- Manages user data: create, update, delete operations
- Stores admin, doctor, and patient data

### admin/admincontroller.py
- Manages all admin panel features
- Doctor schedule management
- User management

### doctor/doctorcontroller.py
- Doctor dashboard functionality
- View personal schedule
- Manage patient queue

### patient/patientcontroller.py
- Patient dashboard functionality
- Find doctors and schedules
- Book appointments

## How to Run

```
python main.py
```

