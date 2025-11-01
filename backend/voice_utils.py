from gtts import gTTS
import os
import speech_recognition as sr
import whisper
import tempfile
from io import BytesIO

# --- Text-to-Speech (Existing) ---

AUDIO_DIR = "data/audio_cache"
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech(text: str) -> bytes | None:
    """
    Converts a string of text into MP3 audio bytes using gTTS.
    Returns the audio as bytes, not a file path, so Streamlit can serve it directly.
    """
    try:
        # Create audio in memory using BytesIO
        audio_buffer = BytesIO()
        tts = gTTS(text=text, lang='en', slow=False)
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)  # Reset pointer to beginning
        return audio_buffer.getvalue()  # Return the bytes
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None

# --- Speech-to-Text (New) ---

# Load the whisper model. This happens once when the app starts.
# 'base' is a good balance of speed and accuracy for local use.
try:
    print("Loading Whisper 'base' model (this may take a moment)...")
    whisper_model = whisper.load_model("base")
    print("Whisper model loaded successfully.")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    whisper_model = None

def transcribe_audio_from_mic() -> str | None:
    """
    Listens for audio from the microphone, saves it to a temp file,
    transcribes it using Whisper, and returns the text.
    """
    if not whisper_model:
        print("Whisper model is not loaded. Cannot transcribe.")
        return None
        
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        
        try:
            # Listen for audio. Adjust timeouts as needed.
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("Listening timed out waiting for phrase to start.")
            return None

    print("Audio captured. Transcribing...")
    
    try:
        # Save audio to a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio.get_wav_data())
            tmp_filepath = tmp_file.name

        # Transcribe using Whisper
        result = whisper_model.transcribe(tmp_filepath, fp16=False) # fp16=False if not on GPU
        transcribed_text = result["text"]
        
        print(f"Transcribed: {transcribed_text}")
        
        # Clean up the temp file
        os.remove(tmp_filepath)
        
        if not transcribed_text.strip():
            return None # Return None if transcription is empty
            
        return transcribed_text
        
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
        return None
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None