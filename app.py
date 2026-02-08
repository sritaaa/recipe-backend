from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import uuid
import glob
from faster_whisper import WhisperModel

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio_tmp")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Load Whisper model ONCE (important)
# Options: "tiny", "base", "small"
model = WhisperModel(
    "base",               # good balance
    device="cpu",         # use "cuda" if you have GPU
    compute_type="int8"   # fast + low memory
)

# ---------------- APP ----------------
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Local Whisper Backend Running ✅"

@app.route("/get-transcript", methods=["POST"])
def get_transcript():
    try:
        data = request.json
        youtube_url = data.get("url")

        if not youtube_url:
            return jsonify({"success": False, "error": "No URL provided"}), 400

        uid = str(uuid.uuid4())
        output_template = os.path.join(AUDIO_DIR, uid)

        # Download audio
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Find mp3
        mp3_files = glob.glob(os.path.join(AUDIO_DIR, f"{uid}*.mp3"))
        if not mp3_files:
            return jsonify({
                "success": False,
                "error": "Audio conversion failed"
            }), 500

        audio_path = mp3_files[0]

        # ---------------- WHISPER ----------------
        segments, info = model.transcribe(audio_path)

        transcript_text = ""
        for segment in segments:
            transcript_text += segment.text + " "

        # Cleanup
        os.remove(audio_path)

        return jsonify({
            "success": True,
            "language": info.language,
            "transcript": transcript_text.strip()
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

