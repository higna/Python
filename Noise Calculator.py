import pyaudio
import numpy as np
import sounddevice as sd
import time

# Audio input settings
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1              # Mono channel
RATE = 44100              # Sampling rate
CHUNK = 1024              # Buffer size
THRESHOLD = 35.0          # Threshold in dB for loud audio detection
BEEP_DURATION = 0.2       # Duration of the beep sound in seconds

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Function to generate a beep sound
def beep():
    beep_freq = 1000  # Frequency of the beep sound
    beep_duration = BEEP_DURATION  # Duration of the beep sound
    sample_rate = 44100  # Sample rate

    t = np.linspace(0, beep_duration, int(beep_duration * sample_rate), endpoint=False)
    beep_signal = 0.5 * np.sin(2 * np.pi * beep_freq * t)
    sd.play(beep_signal, samplerate=sample_rate)
    sd.wait()

# Open the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")
def calculate_decibels(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    print(audio_data[:10])  # Print first few samples to verify
    rms = np.sqrt(np.mean(np.square(audio_data)))
    rms = rms if rms > 0 else np.finfo(float).eps
    decibels = 20 * np.log10(rms)
    return decibels

try:
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            sound_level = calculate_decibels(data)
            print(f"Sound Level: {sound_level:.2f} dB")

            if sound_level > THRESHOLD:
                beep()

            time.sleep(1)
        except IOError as e:
            print(f"Error reading audio stream: {e}")
except KeyboardInterrupt:
    pass

print("Finished recording")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()
