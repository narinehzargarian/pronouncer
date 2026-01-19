"""Dictionary API integration for pronunciation lookup."""

import tempfile
from typing import Optional, TypedDict

import requests


API_BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"


class Definition(TypedDict):
    part_of_speech: str
    definition: str


class WordResult(TypedDict):
    word: str
    phonetic: str
    audio_url: Optional[str]
    definitions: list[Definition]


def lookup_word(word: str) -> Optional[WordResult]:
    """Look up a word in the dictionary API.

    Args:
        word: The word to look up

    Returns:
        WordResult with pronunciation info, or None if not found
    """
    try:
        response = requests.get(f"{API_BASE_URL}/{word.lower()}", timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    if not data:
        return None

    entry = data[0]

    # Get phonetic text - try multiple sources
    phonetic = entry.get("phonetic", "")
    audio_url = None

    # Look through phonetics array for audio and better phonetic text
    for p in entry.get("phonetics", []):
        if p.get("text") and not phonetic:
            phonetic = p["text"]
        if p.get("audio"):
            audio_url = p["audio"]
            if p.get("text"):
                phonetic = p["text"]
            break

    # Gather definitions
    definitions: list[Definition] = []
    for meaning in entry.get("meanings", []):
        pos = meaning.get("partOfSpeech", "")
        for defn in meaning.get("definitions", [])[:2]:
            definitions.append({
                "part_of_speech": pos,
                "definition": defn.get("definition", ""),
            })

    return {
        "word": entry.get("word", word),
        "phonetic": phonetic or "(no phonetic available)",
        "audio_url": audio_url,
        "definitions": definitions,
    }


def play_pronunciation(audio_url: str) -> bool:
    """Download and play pronunciation audio.

    Args:
        audio_url: URL to the audio file

    Returns:
        True if playback succeeded, False otherwise
    """
    try:
        response = requests.get(audio_url, timeout=10)
        response.raise_for_status()

        # Save to temp file and play
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(response.content)
            temp_path = f.name

        # Try different audio playback methods
        if _play_with_afplay(temp_path):
            return True
        if _play_with_playsound(temp_path):
            return True

        print("  Could not play audio - no audio player available")
        return False

    except requests.RequestException as e:
        print(f"  Could not download audio: {e}")
        return False


def _play_with_afplay(path: str) -> bool:
    """Try to play audio using macOS afplay."""
    import subprocess
    try:
        subprocess.run(["afplay", path], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def _play_with_playsound(path: str) -> bool:
    """Try to play audio using playsound library."""
    try:
        from playsound import playsound
        playsound(path)
        return True
    except Exception:
        return False


def speak_word(word: str) -> bool:
    """Speak a word using text-to-speech (macOS say command).

    Args:
        word: The word to speak

    Returns:
        True if speech succeeded, False otherwise
    """
    import subprocess
    try:
        subprocess.run(["say", word], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
