# 🎙️ Pipecat Voice Assistant

[![Streamlit App](https://img.shields.io/badge/Launch%20App-Streamlit-informational?style=for-the-badge&logo=streamlit)](https://pipecat-va-hakljyonk4mmbaddqsru4t.streamlit.app/)

**Pipecat Voice Assistant** is a modular voice interaction system built using [Pipecat](https://github.com/anysphere/pipecat), an open-source pipelining framework for AI applications. This app demonstrates how you can build a flexible and powerful speech-based assistant in Python by combining:

- 🎤 Speech-to-Text (STT) via Deepgram
- 🧠 Large Language Model (LLM) via Gemini (or GPT/Claude)
- 🔊 Text-to-Speech (TTS) via Kokoro
- 🧩 A plug-and-play modular pipeline architecture using Pipecat

The app runs entirely in your browser thanks to **Streamlit Cloud**, making it ideal for demos, learning projects, or production prototypes.

---

## ✨ Features

- **🎙️ Record Voice** from browser using `st.audio_input`
- **📃 Speech-to-Text** using Deepgram API
- **🤖 LLM response generation** using Gemini or any custom LLM
- **🗣️ Text-to-Speech** using Kokoro’s expressive voice models
- **🔁 Modular Pipeline** using Pipecat processors (`FrameProcessor`, `ConsumerProcessor`)
- **🚀 Deployed on Streamlit Cloud** – no frontend coding needed
- **🧩 Extensible and Swappable** – plug in your own STT, LLM, or TTS

---

## 🧠 Pipecat Pipeline Architecture

At its core, this app uses **Pipecat’s processor-based pipeline system** to create a fully asynchronous flow of data. The voice assistant is structured like this:

```text
[ 🎙️ Mic Input ]
      ↓
[ MicInputProducer ]        # Takes Streamlit audio input and wraps it in AudioRawFrame
      ↓
[ STTProcessor ]            # Transcribes speech using Deepgram
      ↓
[ LLMProcessor ]            # Generates response using Gemini/GPT/Groq(models)
      ↓
[ TTSProcessor ]            # Synthesizes speech using Kokoro TTS
      ↓
[ 🔊 Output to Browser ]
```

## 🛠️ Installation (Local)
```
# Clone the repository
git clone https://github.com/Pg158/pipecat-va.git
cd pipecat-va

# Create a virtual environment and activate it
conda create -n pipecat python=3.11
conda activate pipecat

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app locally
streamlit run app.py
```

## 🧾 Requirements
Make sure your requirements.txt includes:
```
streamlit
pipecat
numpy
scipy
soundfile
torch
torchaudio
transformers
huggingface-hub
kokoro
deepgram-sdk==4.6.0
python-dotenv
```
#### ⚠️ Do not include simpleaudio if deploying to Streamlit Cloud — it may cause build errors. Audio is played via st.audio() on the web.
---

## 🌐 Deployment (Streamlit Cloud)
Push your code to a GitHub repository

Go to Streamlit Cloud

Click "New App"

Choose your repo, branch, and set app.py as the entry point

Click "Deploy" and you’re live!

#### Make sure your API keys (Deepgram, Gemini, etc.) are set via Streamlit's secrets manager or .env file (when running locally).
---

## 📜 License
MIT License. This project is for educational, demonstration, and personal use.

---

## 🙋‍♀️ Acknowledgements

Pipecat by Pipecat-ai

Deepgram Speech-to-Text

Kokoro TTS

Streamlit Cloud