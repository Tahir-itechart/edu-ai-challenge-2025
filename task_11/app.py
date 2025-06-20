import os
import sys
import json
import logging
from typing import Dict, Any
from pathlib import Path
import argparse
from pydub import AudioSegment
import openai
from dotenv import load_dotenv


RESULTS_DIR = Path('results')
WHISPER_MODEL = "whisper-1"
GPT_MODEL = "gpt-4.1-mini"


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def load_api_key() -> None:
    """Load environment variables and set OpenAI API key."""
    load_dotenv()
    openai.api_key = os.getenv('TOKEN')
    if not openai.api_key:
        logging.error("OpenAI API key not found in environment variable 'TOKEN'.")
        sys.exit(1)


def ensure_results_dir() -> None:
    """Ensure the results directory exists."""
    RESULTS_DIR.mkdir(exist_ok=True)


def get_audio_duration(audio_path: Path) -> float:
    """Return the duration of the audio file in seconds using pydub. Raise a clear error if format is unsupported."""
    try:
        audio = AudioSegment.from_file(str(audio_path))
        return audio.duration_seconds
    except Exception as e:
        logging.error(
            f"Could not read audio file '{audio_path}'. "
            "Make sure the file exists, is a supported format (mp3, wav, m4a, flac, ogg, webm, etc.), "
            "and ffmpeg is installed. Error: {e}"
        )
        sys.exit(1)


def transcribe_audio(audio_path: Path) -> str:
    """Transcribe audio using OpenAI Whisper API. Raise a clear error if format is unsupported."""
    logging.info(f"Transcribing {audio_path} using OpenAI Whisper...")
    try:
        with audio_path.open("rb") as audio_file:
            transcript_response = openai.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                response_format="text"
            )
        return transcript_response
    except Exception as e:
        logging.error(
            f"Could not transcribe audio file '{audio_path}'. "
            "Make sure the file is a supported format for OpenAI Whisper. Error: {e}"
        )
        sys.exit(1)


def summarize_text(text: str) -> str:
    """Summarize text using OpenAI GPT model, requesting a short summary if possible."""
    logging.info("Summarizing transcription using OpenAI GPT (short summary)...")
    try:
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
                {"role": "user", "content": f"Summarize the following transcript as briefly as possible, focusing only on the most important points:\n{text}"}
            ],
            max_tokens=150,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        sys.exit(1)


def get_word_count(transcript: str) -> int:
    """Count the number of words in the transcript."""
    return len(transcript.split())


def get_speaking_speed_wpm(word_count: int, duration_sec: float) -> float:
    """Calculate speaking speed in words per minute."""
    return word_count / (duration_sec / 60) if duration_sec > 0 else 0


def gpt_topics(transcript: str) -> list:
    """Use GPT to extract a list of frequently mentioned topics from the transcript."""
    logging.info("Extracting topics using GPT (deterministic)...")
    try:
        prompt = (
            "Given the following transcript, extract a list of the most frequently mentioned topics. "
            "Return the result as a JSON list of objects with 'topic' and 'mentions'. "
            "For topic labeling, group related phrases under a single, clear label, and count all relevant mentions. "
            "Return only the JSON list.\n\n"
            f"Transcript:\n{transcript[:2000]}\n\n"
        )
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at extracting topics from meeting transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        start = content.find('[')
        end = content.rfind(']') + 1
        topics = json.loads(content[start:end])
        return topics
    except Exception as e:
        logging.error(f"Error during GPT topic extraction: {e}")
        return []


def analytics(transcript: str, duration_sec: float) -> dict:
    """Hybrid analytics: word count and WPM in Python, topics by GPT."""
    word_count = get_word_count(transcript)
    wpm = get_speaking_speed_wpm(word_count, duration_sec)
    topics = gpt_topics(transcript)
    return {
        "word_count": word_count,
        "speaking_speed_wpm": int(wpm),
        "frequently_mentioned_topics": topics
    }


def get_result_subdir(audio_path: Path) -> Path:
    """Return the subdirectory in results named after the audio file (without extension).
    If it exists, ask user to overwrite or create a new folder with a numeric postfix."""
    ensure_results_dir()
    base_name = audio_path.stem
    subdir = RESULTS_DIR / base_name
    if subdir.exists():
        postfix = 2
        while (RESULTS_DIR / f"{base_name}_{postfix}").exists():
            postfix += 1
        print(f"Results for '{base_name}' already exist in: {subdir}")
        choice = input(f"Do you want to overwrite (o) or save as new (n)? [o/n]: ").strip().lower()
        if choice == 'n':
            subdir = RESULTS_DIR / f"{base_name}_{postfix}"
    subdir.mkdir(exist_ok=True)
    return subdir


def save_transcription(transcript: str, subdir: Path) -> Path:
    path = subdir / "transcription.md"
    with path.open('w') as f:
        f.write(transcript.strip() + "\n")
    return path


def save_summary(summary: str, subdir: Path) -> Path:
    path = subdir / "summary.md"
    with path.open('w') as f:
        f.write(summary.strip() + "\n")
    return path


def save_analysis(analytics: Dict[str, Any], subdir: Path) -> Path:
    path = subdir / "analysis.json"
    with path.open('w') as f:
        json.dump(analytics, f, indent=2)
    return path


def process_audio_file(audio_path: str) -> None:
    """Process the audio file: transcribe, summarize, analyze, and save results."""
    audio_path = Path(audio_path)
    if not audio_path.is_file():
        logging.error(f"File not found: {audio_path}")
        sys.exit(1)
    duration_sec = get_audio_duration(audio_path)
    transcript = transcribe_audio(audio_path)
    summary = summarize_text(transcript)
    analytics_result = analytics(transcript, duration_sec)
    subdir = get_result_subdir(audio_path)
    transcript_path = save_transcription(transcript, subdir)
    summary_path = save_summary(summary, subdir)
    analysis_path = save_analysis(analytics_result, subdir)
    print(f"\nTranscription saved to: {transcript_path}")
    print(f"Summary saved to: {summary_path}")
    print(f"Analysis saved to: {analysis_path}")
    print("\nSummary:\n", summary)
    print("\nAnalytics:\n", json.dumps(analytics_result, indent=2))


def main():
    setup_logging()
    load_api_key()
    parser = argparse.ArgumentParser(description="Transcribe, summarize, and analyze an audio file.")
    parser.add_argument('audio_path', nargs='?', help='Path to the audio file')
    args = parser.parse_args()
    audio_path = args.audio_path or input("Enter path to audio file: ").strip()
    process_audio_file(audio_path)


if __name__ == "__main__":
    main() 