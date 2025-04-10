# speech_handler.py

import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

def speech_to_text():
    """Convert spoken words to text."""
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = recognizer.recognize_once()
    return result.text

def text_to_speech(text):
    """Convert text to speech output."""
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text).get()  # <-- Added `.get()` to ensure it completes
