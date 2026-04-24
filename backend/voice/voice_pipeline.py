import whisper
import subprocess
import requests
import time

RECORD_SCRIPT = "/mnt/c/Users/kamal/Desktop/projects/nl2rc-robotics/record_audio.py"
AUDIO_FILE = "/mnt/c/Users/kamal/Desktop/projects/nl2rc-robotics/audio_input.wav"
API_URL = "http://127.0.0.1:8000/command"

def record_audio():
    print("🎤 Recording shuru ho rahi hai...")
    subprocess.run(["python3", RECORD_SCRIPT], check=True)
    print("✅ Recording complete!")

def transcribe_audio():
    print("🔄 Transcribing...")
    model = whisper.load_model("tiny")
    result = model.transcribe(AUDIO_FILE, language="en")
    text = result["text"].strip()
    print(f"📝 Tumne bola: {text}")
    return text

def send_to_api(text):
    print(f"🚀 FastAPI ko bhej raha hai: {text}")
    response = requests.post(API_URL, json={"text": text})
    print(f"✅ Response: {response.json()}")

if __name__ == "__main__":
    record_audio()
    text = transcribe_audio()
    send_to_api(text)