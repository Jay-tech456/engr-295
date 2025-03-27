import whisper
import pyaudio
import numpy as np
import time
import wave

def main():
    # Initialize the Whisper model
    model = whisper.load_model("base")  # You can use "small", "medium", or "large" based on your need

    # Set up PyAudio to capture audio from the microphone
    p = pyaudio.PyAudio()

    # Audio format settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    # Function to record audio in real-time
    def record_audio():
        print("Recording...")
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Recording Finished.")
        stream.stop_stream()
        stream.close()

        # Save the audio to a file
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    # Function to transcribe audio to text using Whisper
    def transcribe_audio():
        # Load and transcribe the recorded audio file
        audio = whisper.load_audio(WAVE_OUTPUT_FILENAME)
        audio = whisper.pad_or_trim(audio)

        # Perform transcription
        result = model.transcribe(audio)
        print(f"Transcription: {result['text']}")

    # Main loop for real-time processing
    while True:
        record_audio()  # Record audio
        transcribe_audio()  # Transcribe the recorded audio
        time.sleep(1)  # Delay to simulate real-time processing

if __name__ == "__main__":
    main()
