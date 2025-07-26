import asyncio
import simpleaudio as sa

from pipecat.frames.frames import AudioRawFrame
from modules.audio import record_until_silence
from modules.custom_services import (
    deepgram_stt_service,
    gemini_llm_service,
    kokoro_tts_service,
    get_audio_properties
)

async def run_conversation():
    print("Starting voice assistant. Say something!")

    while True:
        audio_bytes = record_until_silence()
        input_frame = AudioRawFrame(audio=audio_bytes, sample_rate=16000, num_channels=1)

        text_frame = await deepgram_stt_service(input_frame)
        user_text = text_frame.text.strip()
        if not user_text:
            print("Didn't catch that, please try again.")
            continue

        print(f"You said: {user_text}")

        response_frame = await gemini_llm_service(text_frame)
        response_text = response_frame.text.strip()
        print(f"Assistant: {response_text}")

        output_frame = await kokoro_tts_service(response_frame)

        props = get_audio_properties(output_frame.audio)

        play_obj = sa.play_buffer(
            output_frame.audio,
            num_channels=props["num_channels"],
            bytes_per_sample=props["bytes_per_sample"],
            sample_rate=props["sample_rate"]
        )
        play_obj.wait_done()

if __name__ == "__main__":
    asyncio.run(run_conversation())
