# modules/tts.py

import io
import numpy as np
import soundfile as sf
from kokoro import KPipeline

# Initialize the Kokoro TTS pipeline (lang_code "a" = American English)
pipeline = KPipeline(lang_code="a")

def synthesize_speech(text: str, voice: str = "af_heart") -> bytes:
    """
    Synthesizes speech using Kokoro TTS and returns WAV bytes.
    """
    # Generate audio chunks from text
    audio_chunks = pipeline(text, voice=voice)
    
    # Concatenate all chunks
    full_audio = np.concatenate([chunk for _, _, chunk in audio_chunks])
    
    # Save as WAV in memory
    wav_io = io.BytesIO()
    sf.write(wav_io, full_audio, 24000, format="WAV")
    wav_io.seek(0)
    
    return wav_io.read()
