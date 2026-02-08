from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Recipe Backend API is running! ✅"

@app.route('/get-transcript', methods=['GET', 'POST'])
def get_transcript():
    try:
        # Read URL
        if request.method == 'POST':
            data = request.json or {}
            video_url = data.get('url', '')
        else:
            video_url = request.args.get('url', '')

        if not video_url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400

        # Extract video ID
        match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', video_url)
        if not match:
            return jsonify({'success': False, 'error': 'Invalid YouTube URL'}), 400

        video_id = match.group(1)

        # 🔑 EXACTLY like Streamlit app
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Prefer English
        try:
            transcript_obj = transcript_list.find_manually_created_transcript(['en'])
        except:
            transcript_obj = transcript_list.find_generated_transcript(['en'])

        transcript_data = transcript_obj.fetch()
        transcript = " ".join(item['text'] for item in transcript_data)

        return jsonify({
            'success': True,
            'video_id': video_id,
            'language': transcript_obj.language,
            'is_generated': transcript_obj.is_generated,
            'transcript': transcript
        })

    except (TranscriptsDisabled, NoTranscriptFound):
        return jsonify({
            'success': False,
            'error': 'Transcript exists on YouTube but cannot be accessed programmatically'
        }), 404

    except VideoUnavailable:
        return jsonify({
            'success': False,
            'error': 'Video unavailable'
        }), 404

    except Exception as e:
        print("SERVER ERROR:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

