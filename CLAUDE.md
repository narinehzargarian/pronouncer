# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Run the CLI
pronouncer <word>              # Look up a word
pronouncer <word> -p           # Look up and play audio
pronouncer -i                  # Interactive mode
pronouncer -i -p               # Interactive mode with audio
```

## Architecture

This is a Python CLI tool that fetches pronunciation data from the Free Dictionary API (dictionaryapi.dev).

- `src/pronouncer/cli.py` - Entry point and argument parsing
- `src/pronouncer/dictionary.py` - API integration and audio playback

The app uses the Free Dictionary API which returns phonetic transcription (IPA) and audio URLs. For words not in the dictionary (company names, brand names, etc.), it falls back to macOS text-to-speech (`say` command). Audio playback uses `afplay` on macOS.
