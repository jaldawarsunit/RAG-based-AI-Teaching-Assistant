#video files to MP3
import os
import subprocess
files=os.listdir("videos")
for file in files:
    tutorial_number=file.split(" ")[0] # based on what to name use or modify
    file_name=file.split(".")[0].split(" ")[1]
    # check="ffmpeg"+"-i"+f"videos/{file}"+f"audios/{tutorial_number} {file_name}.mp3"
    subprocess.run(["ffmpeg","-i",f"videos/{file}",f"audios/{tutorial_number} {file_name}.mp3"])    
