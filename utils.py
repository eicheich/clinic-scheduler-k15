from datetime import datetime, timedelta
from models import DataManager

class ScheduleUtils:
    def __init__(self):
        self.data_manager = DataManager()

    def get_available_doctors(self):
        doctors_data = self.data_manager.load_data(self.data_manager.doctors_file)
        return doctors_data.get("doctors", [])

    def get_doctor_schedule(self, doctor_id):
        schedules_data = self.data_manager.load_data(self.data_manager.schedules_file)
        for schedule in schedules_data.get("schedules", []):
            if schedule["doctor_id"] == doctor_id:
                return schedule
        return None

    def create_time_slots(self, start_time, end_time, duration_minutes=30):
        time_slots = []
        current_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")
        
        while current_time < end_time:
            time_slots.append({
                "time": current_time.strftime("%H:%M"),
                "available": True,
                "patient": None
            })
            current_time += timedelta(minutes=duration_minutes)
        
        return time_slots

    def filter_expired_slots(self, schedule):
        today = datetime.now().date()
        schedule_date = datetime.strptime(schedule["date"], "%Y-%m-%d").date()
        
        if schedule_date < today:
            return False
        
        time_slots = []
        for slot in schedule["time_slots"]:
            slot_time = datetime.strptime(slot["time"], "%H:%M").time()
            slot_datetime = datetime.combine(schedule_date, slot_time)
            
            if slot_datetime > datetime.now():
                time_slots.append(slot)
        
        schedule["time_slots"] = time_slots
        return True
