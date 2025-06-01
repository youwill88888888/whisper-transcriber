import whisper
from fastapi import FastAPI, Request
from pydantic import BaseModel
import yt_dlp
import uuid
import os

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

@app.post("/transcribe")
async def transcribe_video(req: VideoRequest):
    video_url = req.video_url
    video_path = f"/tmp/{uuid.uuid4()}.mp4"

    ydl_opts = {
        'outtmpl': video_path,
        'quiet': True,
        'format': 'best[ext=mp4]/mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        return {"error": f"Failed to download video: {str(e)}"}

    try:
        model = whisper.load_model("base")
        result = model.transcribe(video_path)
        os.remove(video_path)
        return {
            "text": result["text"],
            "language": result["language"],
            "duration": result["duration"]
        }
    except Exception as e:
        return {"error": f"Failed to transcribe video: {str(e)}"}