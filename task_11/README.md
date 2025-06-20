# Task 11: Audio Transcription, Summarization, and Analytics Console App

## Requirements
- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (required by pydub for most audio formats)
- OpenAI API key
- Python packages: `openai`, `pydub`, `python-dotenv`

## Setup

1. **Create and activate the virtual environment:**

```bash
python3 -m venv env
source env/bin/activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Usage
1. Place your audio file (e.g., `audio.mp3`) in known place.
2. Set your OpenAI API key in a `.env` file:
   ```
   TOKEN=your_openai_api_key_here
   ```
3. Run the app:
   ```
   python app.py path/to/your/audio.mp3
   ```
   Or, if you omit the argument, you will be prompted for the path.

4. The app will:
   - Transcribe the audio
   - Summarize the transcript (short summary)
   - Extract analytics (word count, WPM in Python; topics by GPT)
   - Save the results in a subfolder of `results/` named after the audio file (e.g., `results/audio`):
     - `transcription.md` (full transcript)
     - `summary.md` (short summary)
     - `analysis.json` (analytics)
   - If results for the audio file already exist, you will be prompted to overwrite or save as a new result (e.g., `results/audio_2`).
   - Print the summary and analytics in the console

## Supported Audio Formats
- The app accepts any audio file format supported by [pydub](https://github.com/jiaaro/pydub) (with ffmpeg) and OpenAI Whisper.
- Common formats: mp3, wav, m4a, flac, ogg, webm, and more.
- If you get an error, ensure your file is a valid audio file and ffmpeg is installed.

## Example Analytics Output
```
{
  "word_count": 1280,
  "speaking_speed_wpm": 132,
  "frequently_mentioned_topics": [
    { "topic": "Customer Onboarding", "mentions": 6 },
    { "topic": "Q4 Roadmap", "mentions": 4 },
    { "topic": "AI Integration", "mentions": 3 }
  ]
}
``` 