import os
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write

# Lazy-loaded — model is only pulled into memory the first time record_voice() is called.
# This means app startup is fast even when voice is never used.
_model = None


def _get_model():
    global _model
    if _model is None:
        import whisper  # imported here so the heavy load is deferred
        _model = whisper.load_model("base")
    return _model


def record_voice(seconds: int = 5, sample_rate: int = 44100) -> str:
    """
    Record audio from the default microphone for `seconds` seconds,
    transcribe with Whisper, and return the recognised text.

    Raises RuntimeError if recording or transcription fails.
    """
    try:
        recording = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,          # mono is sufficient for speech
            dtype="int16",
        )
        sd.wait()
    except Exception as e:
        raise RuntimeError(f"Microphone recording failed: {e}") from e

    # Write to a temp file so we don't litter the working directory
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        write(tmp.name, sample_rate, recording)
        model = _get_model()
        result = model.transcribe(tmp.name)
        return result["text"].strip()
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}") from e
    finally:
        tmp.close()
        os.unlink(tmp.name)  # clean up temp file regardless of outcome