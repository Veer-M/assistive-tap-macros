# Assistive tap macros

This turns groups of microphone taps into copy and paste shortcuts. Two taps copy, and three taps paste. A replay mode lets you check the timing without touching the keyboard.

## Run it

Use Python 3.11 or newer. Run these commands from this repository's folder.

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate
python -m pip install -r requirements.txt
```

```sh
python tap_macros.py --replay sample_taps.json
# Live microphone (install requirements-live.txt first):
python tap_macros.py
python tap_macros.py --execute
```

## How it works and current limits

Actions wait for 0.8 seconds of quiet after the final tap, so a third tap can arrive before copy fires. A sustained loud sound counts once until the volume falls below the low threshold. A 1.5-second idle gap discards stale taps. Default live mode only prints actions. --execute sends Ctrl+C/Ctrl+V to the focused app. RMS uses NumPy because audioop was removed in Python 3.13. This runs in a terminal rather than installing a background service.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests check two and three taps, sustained noise, idle reset, and PCM volume calculation. Live microphone sensitivity needs adjustment for your setup.

For microphone use, install `python -m pip install -r requirements-live.txt`. PyAudio needs PortAudio; on some Linux systems install the PortAudio development package first. Use `--help` for all options.
