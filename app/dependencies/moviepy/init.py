import os
from os.path import splitext
import moviepy.editor as mp
from enums.file_type import FileType
import ffmpeg


def convert_video_to_audio(path_file: str) -> str:
  name_file: str = splitext(os.path.basename(path_file))[0]
  
  bitrate = get_bitrate(path_file)

  clip = mp.VideoFileClip(path_file)

  path_new_audio: str = FileType.get_file_path(FileType.AUDIO.value, f"{name_file}.mp3")

  clip.audio.write_audiofile(path_new_audio, bitrate=bitrate)

  return path_new_audio


def get_bitrate(file: str) -> str: # str | None
  try:
    probe = ffmpeg.probe(file)
    video_bitrate = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
    bitrate = int(int(video_bitrate['bit_rate']) / 1000)
    return f"{bitrate}k"
  except:
    return None