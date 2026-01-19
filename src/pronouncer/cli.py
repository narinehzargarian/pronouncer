#!/usr/bin/env python3
"""CLI interface for pronouncer."""

import argparse
import sys

from pronouncer.dictionary import lookup_word, play_pronunciation, speak_word


def main():
    parser = argparse.ArgumentParser(
        prog="pronouncer",
        description="Get pronunciation of English words from the command line",
    )
    parser.add_argument("word", nargs="?", help="Word to look up")
    parser.add_argument(
        "-p", "--play", action="store_true", help="Play audio pronunciation"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Interactive mode"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode(args.play)
    elif args.word:
        lookup_and_display(args.word, args.play)
    else:
        parser.print_help()
        sys.exit(1)


def lookup_and_display(word: str, play_audio: bool = False):
    """Look up a word and display its pronunciation."""
    result = lookup_word(word)

    if result is None:
        print(f"\n  {word}")
        print(f"  (not in dictionary - using text-to-speech)")
        print()
        if play_audio:
            speak_word(word)
        return

    print(f"\n  {result['word']}")
    print(f"  {result['phonetic']}")

    if result["definitions"]:
        print(f"\n  Definitions:")
        for i, defn in enumerate(result["definitions"][:3], 1):
            print(f"    {i}. ({defn['part_of_speech']}) {defn['definition']}")

    print()

    if play_audio and result["audio_url"]:
        play_pronunciation(result["audio_url"])
    elif play_audio and not result["audio_url"]:
        speak_word(word)


def interactive_mode(play_audio: bool = False):
    """Run in interactive mode, accepting multiple words."""
    print("Pronouncer - Interactive Mode")
    print("Type a word to get its pronunciation, or 'quit' to exit\n")

    while True:
        try:
            word = input(">>> ").strip()
            if not word:
                continue
            if word.lower() in ("quit", "exit", "q"):
                break
            lookup_and_display(word, play_audio)
        except (KeyboardInterrupt, EOFError):
            print()
            break


if __name__ == "__main__":
    main()
