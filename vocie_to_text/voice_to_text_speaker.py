import os
import queue
import pyaudio
from google.cloud import speech

# Set up Google API credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jianpengyuan/Desktop/engr/engr-295/vocie_to_text/sa_speech_demo.json"

# Audio stream parameters
RATE = 16000  # Sample rate in Hz
CHUNK = int(RATE / 10)  # 100ms chunks

# Queue to store audio data
audio_queue = queue.Queue()

# Callback function to read audio stream
def audio_callback(in_data, frame_count, time_info, status_flags):
    audio_queue.put(in_data)
    return None, pyaudio.paContinue

# Start PyAudio stream
audio_interface = pyaudio.PyAudio()
stream = audio_interface.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK,
                              stream_callback=audio_callback)

# Google Speech-to-Text client
client = speech.SpeechClient()

# ✅ Use SpeakerDiarizationConfig instead of enable_speaker_diarization
diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,  # Minimum expected speakers
    max_speaker_count=2   # Maximum expected speakers
)

# ✅ Updated RecognitionConfig
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code="en-US",
    diarization_config=diarization_config  # ✅ Use diarization_config field
)

streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

# Function to stream audio
def generate_audio():
    while True:
        chunk = audio_queue.get()
        if chunk is None:
            break
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

# Process real-time transcription
responses = client.streaming_recognize(streaming_config, generate_audio())

# Print results with speaker tags
for response in responses:
    for result in response.results:
        if result.alternatives:
            transcript = result.alternatives[0].transcript
            print(f"Transcript: {transcript}")
            for word in result.alternatives[0].words:
                print(f"Speaker {word.speaker_tag}: {word.word}")

# Stop the stream
stream.stop_stream()
stream.close()
audio_interface.terminate()
