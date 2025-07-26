import streamlit as st
import io
import asyncio

from pipecat.pipeline.pipeline import Pipeline
from pipecat.processors.frame_processor import FrameProcessor
from pipecat.processors.consumer_processor import ConsumerProcessor

from pipecat.frames.frames import AudioRawFrame, TextFrame

from modules.stt import transcribe_audio
from modules.llm import ask_llama
from modules.tts import synthesize_speech

class MicInputProducer(FrameProcessor):
    def __init__(self, audio_bytes):
        super().__init__()
        self.audio_bytes = audio_bytes
        self._produced = False

    async def process(self, frame=None):
        if not self._produced and self.audio_bytes:
            self._produced = True
            return AudioRawFrame(audio=self.audio_bytes, sample_rate=44100, num_channels=1)
        return None

class STTProcessor(FrameProcessor):
    async def process(self, frame: AudioRawFrame) -> TextFrame:
        from tempfile import NamedTemporaryFile
        import os

        with NamedTemporaryFile(suffix=".wav", delete=False) as temp:
            temp.write(frame.audio)
            temp.flush()
            path = temp.name

        try:
            text = transcribe_audio(path)
        finally:
            os.remove(path)

        return TextFrame(text=text)

class LLMProcessor(FrameProcessor):
    async def process(self, frame: TextFrame) -> TextFrame:
        response = ask_llama(frame.text)
        return TextFrame(text=response)

class TTSProcessor(ConsumerProcessor):
    async def consume(self, frame: TextFrame):
        audio_bytes = synthesize_speech(frame.text)
        st.audio(audio_bytes, format="audio/wav")

st.title("🎙️ Pipecat Voice Assistant (STT + LLM + TTS)")

audio_bytes = st.audio_input("Speak your query...")

if audio_bytes:
    st.write("⏳ Processing...")

    processors=[
        MicInputProducer(audio_bytes),
        STTProcessor(),
        LLMProcessor(),
        TTSProcessor(producer=True)
    ]

    pipeline=Pipeline(processors=processors)

    async def run_pipeline(pipeline):

        input_frame = await processors[0].process(None)

        current_frame = input_frame
        for processor in processors[1:]:
            if hasattr(processor, "process"):
                current_frame = await processor.process(current_frame)
            elif hasattr(processor, "consume"):
                await processor.consume(current_frame)

    asyncio.run(run_pipeline(pipeline))

