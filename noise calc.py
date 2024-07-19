import pyaudio
import numpy as np
import time

# Audio input settings
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1              # Mono channel
RATE = 44100              # Sampling rate
CHUNK = 1024              # Buffer size
RECORD_SECONDS = 5        # Duration to record

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

def calculate_decibels(data):
    # Convert data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Compute RMS (root mean square)
    rms = np.sqrt(np.mean(np.square(audio_data)))
    # Convert RMS to decibels (dB)
    decibels = 20 * np.log10(rms)
    return decibels

try:
    while True:
        # Read audio data
        data = stream.read(CHUNK)
        # Calculate noise level in decibels
        noise_level = calculate_decibels(data)
        print(f"Noise Level: {noise_level:.2f} dB")
        time.sleep(1)  # Delay for 1 second
except KeyboardInterrupt:
    pass

print("Finished recording")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()