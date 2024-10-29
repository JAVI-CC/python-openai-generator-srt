import json
import os
from os.path import splitext
from datetime import timedelta
from dependencies.root_dir import ROOT_DIR
import argostranslate.translate

LANG_AUTOMATIC: str = "Automatic detection"
CURRENT_DIR: str = os.path.dirname(__file__)
FILE_LANGUAGES: str = f"{CURRENT_DIR}/languages_available.json"
SUBTITLES_PATH: str = f"{ROOT_DIR}/data/subtitles"


def get_from_langs_list() -> list:
  with open(FILE_LANGUAGES) as json_file:
    data: dict = json.load(json_file)
    from_langs_list: list = [i['name'] for i in data]
    from_langs_list.insert(0, LANG_AUTOMATIC)

    return from_langs_list


def get_to_langs_list(name_lang: str) -> list:
  with open(FILE_LANGUAGES) as json_file:
    data: dict = json.load(json_file)

    try:
      selected_lang: dict = next(
        lang for lang in data if lang["name"] == name_lang)
    except:
      raise Exception("The selected language is not available!")
    else:
      to_langs_list: list = [i['name'] for i in selected_lang['targets']]

    return to_langs_list


def find_name_lang_by_code(code_lang: str) -> str:
  with open(FILE_LANGUAGES) as json_file:
    data: dict = json.load(json_file)

    try:
      selected_lang: dict = next(
        lang for lang in data if lang["code"] == code_lang)
    except:
      raise Exception("The selected language is not available!")

    return selected_lang["name"]


def translate_text(text: str, from_lang: str, to_lang: str) -> str:
    # Load installed languages
  installed_languages = argostranslate.translate.get_installed_languages()

  # Select source and target languages
  from_lang = next(
    (lang for lang in installed_languages if lang.name == from_lang), None)
  to_lang = next(
    (lang for lang in installed_languages if lang.name == to_lang), None)

  if not from_lang or not to_lang:
    raise Exception("The language not found or language not installed!")

  # Get the translation model for the desired language pair
  translate = from_lang.get_translation(to_lang)

  # Translate text
  translated_text = translate.translate(text)

  return translated_text


def generate_subtitles(segments: list, from_lang: str, to_lang: str, name_file: str) -> str:
  name_file = f"{splitext(name_file)[0]} ({to_lang}).srt"
  for segment in segments:
    start_time: str = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
    end_time: str = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'

    text: str = segment['text']
    segment_id: int = segment['id'] + 1

    if text[0] == ' ':
      text_res: str = translate_text(text[1:], from_lang, to_lang)
    else:
      text_res: str = translate_text(text, from_lang, to_lang)

    segment: str = f"{segment_id}\n{start_time} --> {end_time}\n{text_res}\n\n"

    srt_file_path = os.path.join(SUBTITLES_PATH, name_file)
    with open(srt_file_path, 'a', encoding='utf-8') as srt_file:
      srt_file.write(segment)

  return f"{SUBTITLES_PATH}/{name_file}"
