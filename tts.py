from TTS.api import TTS
import sounddevice as sd


def text_to_speech(text, speaker_id="p225"):

   # Load the model (CPU mode)
   tts = TTS("tts_models/en/vctk/vits", gpu=False)

   # Generate the waveform
   wav = tts.tts(text, speaker=speaker_id)

   # Play the audio
   sd.play(wav, samplerate=tts.synthesizer.output_sample_rate)
   sd.wait()

