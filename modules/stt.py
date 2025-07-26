from deepgram import DeepgramClient
from deepgram.client import DeepgramClientOptions
from utils.api_keys import DEEPGRAM_API_KEY

options = DeepgramClientOptions(verbose=False)

dg_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

def transcribe_audio(audio_path: str) -> str:
    with open(audio_path, "rb") as file:
        response = dg_client.listen.prerecorded.v("1").transcribe_file(
            source={"buffer": file, "mimetype": "audio/wav"}
        )


    
    try:
        alternatives = response["results"]["channels"][0]["alternatives"]
        if not alternatives:
            return ""  # No transcription found

        transcript = alternatives[0]["transcript"]
        return transcript.strip()

    except (KeyError, IndexError) as e:
        print("Deepgram response error:", e)
        return ""

