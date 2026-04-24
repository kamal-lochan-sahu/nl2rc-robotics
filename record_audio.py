import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 16000
DURATION = 5  # 5 seconds record karega
OUTPUT_PATH = r"C:\Users\kamal\Desktop\projects\nl2rc-robotics\audio_input.wav"

print("Recording shuru... 5 seconds bolne ka time hai!")
print("Ab bolo: 'Move forward 2 meters'")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype=np.int16
)
sd.wait()

write(OUTPUT_PATH, SAMPLE_RATE, audio)
print(f"Recording save ho gayi: {OUTPUT_PATH}")