import glob
import time
import os
import re

def cleanup_audio_folder(folder="static/audio", max_age_seconds=3600):
    now = time.time()
    for file in glob.glob(f"{folder}/*.wav"):
        if os.path.isfile(file) and now - os.path.getmtime(file) > max_age_seconds:
            os.remove(file)



def strip_markdown(text):
    # Remove bold/italic/code ticks/headers/links etc.
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # *italic*
    text = re.sub(r"`(.*?)`", r"\1", text)        # `code`
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)  # [text](link)
    text = re.sub(r"#+\s", "", text)              # # headers
    return text
