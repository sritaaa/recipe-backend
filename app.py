from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
CORS(app)  # Allow Android app to access this

@app.route('/', methods=['GET'])
def home():
    return "Recipe Backend API is running! ✅"

@app.route('/get-transcript', methods=['POST'])
def get_transcript():
    try:
        data = request.json
        video_url = data.get('url', '')
        
        # Extract video ID from URL
        video_id_match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', video_url)
        
        if not video_id_match:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        video_id = video_id_match.group(1)
        
        print(f"Fetching transcript for video: {video_id}")
        
        # Get transcript from YouTube
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text segments
        transcript = ' '.join([item['text'] for item in transcript_list])
        
        print(f"Transcript length: {len(transcript)} characters")
        
        return jsonify({
            'success': True,
            'transcript': transcript,
            'video_id': video_id
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)