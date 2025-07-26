import io
import wave
import simpleaudio as sa

from pipecat.frames.frames import AudioRawFrame, TextFrame
from modules.stt import transcribe_audio
from modules.llm import ask_llama
from modules.tts import synthesize_speech
import tempfile
import os

async def deepgram_stt_service(frame: AudioRawFrame) -> TextFrame:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
        temp.write(frame.audio)
        temp.flush()
        temp_path = temp.name

    try:
        text = transcribe_audio(temp_path)
    finally:
        os.remove(temp_path)

    return TextFrame(text=text)

async def llama_llm_service(frame: TextFrame) -> TextFrame:
    response = ask_llama(frame.text)
    return TextFrame(text=response)

def get_audio_properties(audio_bytes: bytes):
    with wave.open(io.BytesIO(audio_bytes), 'rb') as wav:
        return {
            "sample_rate": wav.getframerate(),
            "num_channels": wav.getnchannels(),
            "bytes_per_sample": wav.getsampwidth()
        }

async def kokoro_tts_service(frame):
    audio = synthesize_speech(frame.text)
    return AudioRawFrame(
        audio=audio, 
        sample_rate=24000, 
        num_channels=1
    )
