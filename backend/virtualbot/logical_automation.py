# logic_automation.py
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Logic App endpoints
REMINDER_WEBHOOK_URL = os.getenv("AZURE_LOGIC_APP_REMINDER_WEBHOOK")
APPOINTMENT_WEBHOOK_URL = os.getenv("AZURE_LOGIC_APP_APPOINTMENT_WEBHOOK")

def send_medication_reminder(patient_email, patient_name, medication_name, reminder_time, reminder_message=""):
    """Trigger Logic App to send medication reminder email"""
    payload = {
        "patientEmail": patient_email,
        "patientName": patient_name,
        "medicationName": medication_name,
        "reminderTime": reminder_time,
        "reminderMessage": reminder_message
    }
    
    try:
        response = requests.post(REMINDER_WEBHOOK_URL, json=payload)
        if response.status_code in [200, 201, 202]:
            return {"success": True, "status": response.status_code}
        else:
            print(f"Error triggering Logic App: {response.status_code} - {response.text}")
            return {"success": False, "error": f"Status code: {response.status_code}"}
    except Exception as e:
        print(f"Exception sending reminder: {e}")
        return {"success": False, "error": str(e)}

def schedule_appointment_notification(patient_email, patient_name, doctor_name, appointment_date, appointment_time, location):
    """Trigger Logic App to send appointment notification"""
    payload = {
        "patientEmail": patient_email,
        "patientName": patient_name,
        "doctorName": doctor_name,
        "appointmentDate": appointment_date,
        "appointmentTime": appointment_time,
        "location": location
    }
    
    try:
        response = requests.post(APPOINTMENT_WEBHOOK_URL, json=payload)
        if response.status_code in [200, 201, 202]:
            return {"success": True, "status": response.status_code}
        else:
            print(f"Error triggering Logic App: {response.status_code} - {response.text}")
            return {"success": False, "error": f"Status code: {response.status_code}"}
    except Exception as e:
        print(f"Exception scheduling appointment: {e}")
        return {"success": False, "error": str(e)}