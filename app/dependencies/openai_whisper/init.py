import os
import whisper
from dependencies.argos_translate.init import generate_subtitles
from dependencies.read_env import getenv

# [Tiny, Base, Small, Medium, Large]
print("Loading model, please wait, it may take several minutes...")
model = whisper.load_model(getenv("WHISPER_LOAD_MODEL", "medium"))


def detect_lang_audio(path_audio: str) -> str:
  audio = whisper.load_audio(path_audio)

  # save 30 first seconds audio
  audio = whisper.pad_or_trim(audio)

  mel = whisper.log_mel_spectrogram(audio).to(model.device)

  probs = model.detect_language(mel)[1]

  detect_lang = sorted(probs.items(), key=lambda x: x[1], reverse=True)[0][0]

  return detect_lang


def transcribe_audio(path_file: str, from_lang: str, to_lang: str) -> str:
  name_file: str = os.path.basename(path_file)

  transcribe = model.transcribe(audio=path_file, language=from_lang, verbose=True)

  path_srt = generate_subtitles(transcribe['segments'], from_lang, to_lang, name_file)

  return path_srt
