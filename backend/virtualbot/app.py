# app.py
from flask import Flask, render_template, request, jsonify, session
from gpt_handler import get_gpt_response
from analytics_handler import analyze_health_text, extract_medical_conditions
from speech_handler import speech_to_text, text_to_speech
from db_handler import log_conversation, get_user_conversation_history, save_patient_data
from ehr_fhir import get_patient, get_patient_medications, create_appointment
from logic_automation import send_medication_reminder, schedule_appointment_notification
from healthbot_handler import send_to_health_bot
import uuid
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

@app.route("/")
def home():
    # Generate a user ID if not present
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]
    user_id = session.get("user_id", str(uuid.uuid4()))
    user_role = data.get("role", "patient")  # 'patient' or 'doctor'
    
    # Process message with health analytics
    health_analysis = analyze_health_text(user_message)
    
    # Choose response strategy based on content
    if "appointment" in user_message.lower() or "schedule" in user_message.lower():
        # Appointment handling
        bot_response = "I can help you schedule an appointment. Please provide your preferred date and time."
        # We could trigger Logic App here too
    elif "medication" in user_message.lower() or "reminder" in user_message.lower():
        # Medication reminder
        bot_response = "I'll set a reminder for your medication. What time would you like to be reminded?"
    elif any(term in user_message.lower() for term in ["symptom", "feel", "pain", "hurts"]):
        # Common symptoms - use Health Bot
        health_bot_response = send_to_health_bot(user_id, user_message)
        bot_response = f"Based on our medical database: {health_bot_response}"
    else:
        # General response via GPT
        system_prompt = f"You are a helpful healthcare assistant speaking to a {user_role}. "
        if user_role == "doctor":
            system_prompt += "Provide detailed medical information suitable for healthcare professionals."
        else:
            system_prompt += "Explain medical concepts in simple terms for patients."
            
        bot_response = get_gpt_response(user_message, system_prompt)
    
    # Log the conversation
    log_conversation(user_id, user_message, bot_response, health_analysis)
    
    return jsonify({
        "reply": bot_response,
        "entities": health_analysis["entities"] if health_analysis else [],
        "userId": user_id
    })

@app.route("/speech-to-text", methods=["POST"])
def convert_speech():
    # Process audio file or stream to get text
    # For hackathon, you can simulate this
    text = speech_to_text()
    return jsonify({"text": text})

@app.route("/text-to-speech", methods=["POST"])
def convert_text():
    text = request.json["text"]
    # In a real app, you'd return an audio file
    # For hackathon, you can simulate with browser's speech synthesis
    text_to_speech(text)
    return jsonify({"success": True})

@app.route("/history", methods=["GET"])
def get_history():
    user_id = session.get("user_id", "")
    history = get_user_conversation_history(user_id)
    return jsonify({"history": history})

@app.route("/set-reminder", methods=["POST"])
def set_reminder():
    # Example endpoint for medication reminders
    data = request.json
    result = send_medication_reminder(
        data["email"],
        data["name"],
        data["medication"],
        data["time"],
        data.get("message", "")
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)