import sounddevice as sd
import numpy as np
import webrtcvad
import io
import collections
from scipy.io.wavfile import write

def pcm_to_wav(audio_data,sample_rate=16000):
    wav_buffer = io.BytesIO()
    write(wav_buffer, sample_rate, audio_data)
    wav_buffer.seek(0)
    return wav_buffer.read()

def record_until_silence(sample_rate=16000, frame_duration_ms=30, padding_duration_ms=300, vad_mode=2, max_duration=15):
    vad = webrtcvad.Vad(vad_mode)
    num_padding_frames=int(padding_duration_ms/frame_duration_ms)
    frame_size=int(sample_rate * frame_duration_ms / 1000)
    ring_buffer=collections.deque(maxlen=num_padding_frames)
    triggered=False
    voiced_frames=[]

    def audio_callback(indata, frames, time, status):
        nonlocal triggered, voiced_frames, ring_buffer

        audio_chunk = indata[:, 0]
        raw_bytes = audio_chunk.tobytes()
        is_speech = vad.is_speech(raw_bytes, sample_rate)

        if not triggered:
            ring_buffer.append((raw_bytes, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > 0.8 * ring_buffer.maxlen:
                triggered = True
                for f, _ in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            voiced_frames.append(raw_bytes)
            ring_buffer.append((raw_bytes, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                raise sd.CallbackStop
        
    print("🎙️ Listening (speak to start)...")
    with sd.InputStream(channels=1, samplerate=sample_rate, dtype='int16',
                        blocksize=frame_size, callback=audio_callback):
        sd.sleep(max_duration * 1000)

    print("Speech ended.")

    audio_np = np.frombuffer(b''.join(voiced_frames), dtype=np.int16)
    return pcm_to_wav(audio_np, sample_rate)