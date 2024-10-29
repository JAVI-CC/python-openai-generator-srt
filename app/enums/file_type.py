from enum import Enum

from os import listdir
from os.path import isfile, join, splitext
from dependencies.root_dir import ROOT_DIR


class FileType(Enum):
  AUDIO = "Audio"
  VIDEO = "Video"
  AUDIO_PATH = f"{ROOT_DIR}/data/audios"
  VIDEO_PATH = f"{ROOT_DIR}/data/videos"
  AUDIO_EXTENSIONS = [".mp3", ".ogg"]
  VIDEO_EXTENSIONS = [".mp4", ".mov", ".wmv", ".avi",
                      ".avchd", ".flv", ".mkv", ".webm", ".html5", ".mpeg-2"]

  @classmethod
  def get_files_type_list(cls) -> list:
    return [cls.AUDIO.value, cls.VIDEO.value]

  @classmethod
  def get_files_by_type_list(cls, type: str) -> list:
    my_path: str = f"{cls.AUDIO_PATH.value if type == cls.AUDIO.value else cls.VIDEO_PATH.value}"

    files_list: list = []

    for file in listdir(my_path):
      if isfile(join(my_path, file)) and splitext(file)[1] in (cls.AUDIO_EXTENSIONS.value if type == cls.AUDIO.value else cls.VIDEO_EXTENSIONS.value):
        files_list.append(file)

    if (len(files_list) <= 0):
      raise Exception("Error internal: No file found!")

    return files_list

  @classmethod
  def get_file_path(cls, type, name_file) -> str:
    return f"{cls.AUDIO_PATH.value if type == cls.AUDIO.value else cls.VIDEO_PATH.value}/{name_file}"
