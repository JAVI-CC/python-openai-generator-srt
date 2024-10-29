import inquirer
import time
from dependencies.argos_translate.init import LANG_AUTOMATIC, get_from_langs_list, get_to_langs_list, find_name_lang_by_code
from enums.file_type import FileType
from dependencies.openai_whisper.init import detect_lang_audio, transcribe_audio
from dependencies.moviepy.init import convert_video_to_audio
from dependencies.timer import res_time
from dependencies.storage.init import delete_file

start_time = time.time()

# Question 1
question_1 = [
  inquirer.List("type_file",
                message="Select the file type you want to generate subtitles for?",
                choices=FileType.get_files_type_list()
                )
]
answer_1 = inquirer.prompt(question_1)

# Question 2
question_2 = [
  inquirer.List("file_selected",
                message="Select the file you want to generate subtitles for?",
                choices=FileType.get_files_by_type_list(answer_1["type_file"]),
                )
]
answer_2 = inquirer.prompt(question_2)

# If case video file
path_file: str = FileType.get_file_path(answer_1["type_file"], answer_2["file_selected"])
if (FileType.VIDEO.value == answer_1["type_file"]):
  print("Converting video to audio, please wait, it may take several minutes...")
  path_audio: str = convert_video_to_audio(path_file)

  # Question 2.1
  question_2_1 = [
    inquirer.List("is_keep_file",
                  message="Do you want to keep the new audio file that has been generated?",
                  choices=["No", "Yes"]
                  )
  ]
  answer_2_1 = inquirer.prompt(question_2_1)
else:
  path_audio: str = path_file

# Question 3
question_3 = [
  inquirer.List("from_lang",
                message="Select the language that the file you selected is located in?",
                choices=get_from_langs_list(),
                )
]
answer_3 = inquirer.prompt(question_3)

# If case dectect language
if (LANG_AUTOMATIC == answer_3["from_lang"]):
  code_lang: str = detect_lang_audio(path_audio)
  answer_3["from_lang"] = find_name_lang_by_code(code_lang)
  print(f"\t Language detected: {answer_3['from_lang']}\n")

# Question 4
question_4 = [
  inquirer.List("to_lang",
                message="Select the language you want it to be translated into?",
                choices=get_to_langs_list(answer_3["from_lang"]),
                )
]
answer_4 = inquirer.prompt(question_4)

# Generate subtitles
print("Generating subtitles, please wait, it may take several minutes...")
path_srt = transcribe_audio(path_audio, answer_3["from_lang"], answer_4["to_lang"])

# Delete audio file in case a video has been selected
if (FileType.VIDEO.value == answer_1["type_file"] and answer_2_1["is_keep_file"] == "No"):
  delete_file(path_audio)

end_time = time.time()
print("Subtitles have been generated successfully!")
print(f"Path: {path_srt}")
print(f"Execution time: {res_time(start_time, end_time)}")
