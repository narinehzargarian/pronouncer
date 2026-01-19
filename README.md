# Pronouncer

A command-line tool to get pronunciation of English words, company names, and tech terms.

## Features

- Look up phonetic pronunciation (IPA) for English words
- Play audio pronunciation
- Text-to-speech fallback for words not in the dictionary (company names, brand names, etc.)
- Interactive mode for looking up multiple words

## Installation

```bash
# Using pipx (recommended)
pipx install .

# Or using pip in a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

```bash
# Look up a word
pronouncer entrepreneur

# Look up with audio playback
pronouncer nvidia -p

# Interactive mode
pronouncer -i

# Interactive mode with audio
pronouncer -i -p
```

## Example Output

```
  entrepreneur
  /ˌɑn.trə.prəˈnɝ/

  Definitions:
    1. (noun) A person who organizes and operates a business venture and assumes much of the associated risk.
```

For words not in the dictionary:

```
  nvidia
  (not in dictionary - using text-to-speech)
```

## Requirements

- Python 3.9+
- macOS (for audio playback via `afplay` and `say` commands)

## License

MIT
