import streamlit as st
import simpleaudio as sa
import tempfile

from pipecat.frames.frames import AudioRawFrame


from modules.audio import record_until_silence
from modules.stt import transcribe_audio
from modules.llm import ask_llama
from modules.tts import synthesize_speech

st.set_page_config(page_title="Pipecat Voice Assistant", layout="centered")
st.title("🎙️ Pipecat Voice Assistant")
st.markdown("Speak naturally and let Pipecat respond.")

if st.button("🎤 Start Speaking"):
    st.info("Listening... please speak clearly.")

    audio_bytes = record_until_silence()

    input_frame = AudioRawFrame(audio=audio_bytes, sample_rate=16000, num_channels=1)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

    text = transcribe_audio(temp_path)
    st.markdown(f" **You said:** `{text}`")

    response = ask_llama(text)
    st.markdown(f" **Assistant:** `{response}`")

    audio_response_bytes = synthesize_speech(response)

   
    st.audio(audio_response_bytes, format="audio/wav")
    play_obj = sa.play_buffer(audio_response_bytes, 1, 2, 24000)
    play_obj.wait_done()

    st.success("Done ")
