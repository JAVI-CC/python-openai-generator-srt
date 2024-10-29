import os
from os.path import splitext
import moviepy.editor as mp
from enums.file_type import FileType


def convert_video_to_audio(path_file: str) -> str:
  name_file: str = splitext(os.path.basename(path_file))[0]

  clip = mp.VideoFileClip(path_file)

  path_new_audio: str = FileType.get_file_path(FileType.AUDIO.value, f"{name_file}.mp3")

  clip.audio.write_audiofile(path_new_audio)

  return path_new_audio
