import streamlit as st
from pipecat import pipeline
from pipecat.frames.frames import AudioRawFrame
from modules.custom_services import deepgram_stt_service, gemini_llm_service, kokoro_tts_service

st.title("🎙️ Pipecat Voice Assistant")
st.markdown("Upload your **voice** (WAV format), and this assistant will reply with **speech**, using Pipecat under the hood.")

uploaded_audio = st.file_uploader("Upload a WAV audio file", type=["wav"])

if uploaded_audio:
    st.audio(uploaded_audio, format="audio/wav")

    audio_bytes = uploaded_audio.read()

    with st.spinner("Running Pipecat pipeline..."):

        audio_frame = AudioRawFrame(audio=audio_bytes, sample_rate=16000, num_channels=1)

        pipeline = pipeline(
            services=[
                deepgram_stt_service,
                gemini_llm_service,
                kokoro_tts_service,
            ]
        )

        final_frame = pipeline(audio_frame)

        final_audio = final_frame.audio

    st.success("Here's your assistant's reply:")
    st.audio(final_audio, format="audio/wav")
