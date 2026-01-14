import wave
import io
from piper import PiperVoice
from pydub import AudioSegment

def generate_audio(voice, text_script, audio_filename):

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav_file:
        voice.synthesize_wav(text_script, wav_file)
    wav_buffer.seek(0)

    sound = AudioSegment.from_wav(wav_buffer)
    audio_filename = audio_filename.with_suffix(".mp3")
    sound.export(str(audio_filename), format="mp3", bitrate="320k")

    return audio_filename

