# RecipeXtractor Backend

Flask API server that extracts structured recipes from YouTube cooking videos using Google Gemini 3 and Whisper AI.

## 🎯 Overview

This backend powers the RecipeXtractor Android app by processing YouTube cooking videos and extracting recipes using AI.

**Process:**
1. Downloads audio from YouTube video
2. Converts speech to text using Whisper AI
3. Extracts structured recipe using Gemini 3
4. Returns JSON with ingredients and instructions

## ✨ Features

- 🎬 YouTube audio extraction
- 🎙️ Speech-to-text with Whisper
- 🤖 AI recipe parsing with Gemini 3
- 📋 Structured JSON output
- ⚡ 2-3 minute processing time

## 🛠️ Tech Stack

- Flask (Python)
- Google Gemini 3 API
- OpenAI Whisper
- yt-dlp

## 📋 Prerequisites

- Python 3.8+
- FFmpeg installed
- Google Gemini API Key ([Get it here](https://ai.google.dev/))

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/sritaaa/recipe-backend.git
cd recipe-backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```


### 4. Run Server
```bash
python app.py
```

Server runs at `http://localhost:5000`


## 🧪 Testing

### Using cURL
```bash
curl -X POST http://localhost:5000/extract-recipe \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=EXAMPLE"}'
```

## 🐛 Troubleshooting

**Issue:** FFmpeg not found  
**Solution:** Install FFmpeg
```bash
# Windows
choco install ffmpeg
```

**Issue:** yt-dlp fails  
**Solution:** Update yt-dlp
```bash
pip install --upgrade yt-dlp
```

## 🔗 Related Repositories

- **Android App**: [recipe-extractor-android](https://github.com/sritaaa/recipeXtractor-android)


