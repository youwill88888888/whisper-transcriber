from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import yt_dlp
import whisper
import os

app = FastAPI()
model = whisper.load_model("base")

class VideoRequest(BaseModel):
    video_url: str

def download_video(video_url, out_path="video.mp4"):
    try:
        ydl_opts = {
            'outtmpl': out_path,
            'quiet': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([video_url])
        if not os.path.exists(out_path):
            raise RuntimeError("Download failed: video file not found.")
        return out_path
    except Exception as e:
        raise RuntimeError(f"❌ yt_dlp download error: {str(e)}")

@app.post("/transcribe")
@app.post("/Transcribe")
def transcribe_video(req: VideoRequest):
    try:
        print(f"🎥 Downloading from: {req.video_url}")
        path = download_video(req.video_url)

        if not os.path.isfile(path):
            raise RuntimeError("⚠️ Video file missing after download.")

        result = model.transcribe(path)

        if "text" not in result or not result["text"].strip():
            raise RuntimeError("⚠️ Whisper returned empty text. Possibly no audio.")

        return {
            "text": result["text"],
            "language": result["language"],
            "duration": result["duration"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
