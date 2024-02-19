import pyaudio
import numpy as np

CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Samples per second

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening...")

try:
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        fft_result = np.fft.fft(data)
        freq = np.fft.fftfreq(len(fft_result), 1.0 / RATE)

        # Get the positive frequencies
        positive_freq_mask = freq > 0
        positive_freq = freq[positive_freq_mask]
        hz_freq = positive_freq * RATE

        # Find the dominant frequency
        max_amplitude_index = np.argmax(np.abs(fft_result[positive_freq_mask]))
        dominant_frequency = hz_freq[max_amplitude_index]

        print("Dominant Frequency:", dominant_frequency)

except KeyboardInterrupt:
    print("Finished")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
