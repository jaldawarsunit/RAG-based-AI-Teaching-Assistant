import whisper
import json
import os

model = whisper.load_model("large-v2")
audios=os.listdir("audios")
for audio in audios:
    number=audio.split(" ")[0]
    title=audio.split(".")[0].split(" ")[1]
    print(number,title)

    result = model.transcribe(
        audio=fr"C:/Users/jalda/OneDrive/Desktop/RAG based AI teacher/audios/{audio}",
        # audio=r"C:/Users/jalda/OneDrive/Desktop/RAG based AI teacher/sample.mp3",
        language="hi",  
        task="translate",
        word_timestamps=False
    )
    chunks=[]
    for segments in result["segments"]:
        chunks.append({"number":number,"title":title,"start":segments["start"], "end": segments["end"], "text": segments["text"]}) 

    chunks_with_metadata={"chunks":chunks,"text":result["text"]}

    with open(f"json/{audio}.json","w") as f:
        json.dump(chunks_with_metadata,f)

# # with open("output.json","w") as f:
# #     json.dump(f, result)

# # with open("hindi.txt", "w", encoding="utf-8") as f:
# #     f.write(result["text"])

# # print("Transcription saved to hindi.txt")
