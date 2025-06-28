from TTS.api import TTS
import soundfile as sf
import os
import uuid

def text_to_speech(text, speaker_id="p225"):
    tts = TTS("tts_models/en/vctk/vits", gpu=False)

    wav = tts.tts(text, speaker=speaker_id)

    # Save audio
    filename = f"{uuid.uuid4().hex}.wav"
    filepath = os.path.join("static/audio", filename)
    os.makedirs("static/audio", exist_ok=True)
    sf.write(filepath, wav, samplerate=tts.synthesizer.output_sample_rate)

    return f"/audio/{filename}"  # Return path used in frontend
