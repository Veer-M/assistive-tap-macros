# Assistive tap macros

This program turns microphone taps into copy and paste shortcuts. Two taps mean copy, and three taps mean paste. It gives another way to trigger these actions without pressing the keyboard shortcut yourself.

## How it works

The program measures the volume of small chunks of audio. It uses RMS, or root mean square, to turn the samples into one volume value. A sound above the high threshold counts as a tap. The volume must fall below a lower threshold before another tap can count. This keeps one long sound from counting many times.

After the last tap, the program waits 0.8 seconds without a new tap before choosing an action. This gives a third tap time to arrive before it sends copy. A gap of 1.5 seconds clears an unfinished group if it has not already been handled.

The normal live mode only prints copy or paste. Add `--execute` to send Ctrl+C or Ctrl+V to the app that currently has focus. The program runs in a terminal and stops when you press Ctrl+C there.

## Checking the timing

Replay mode reads a JSON file of times and volume values. It does not use a microphone or send keyboard shortcuts. The included sample should print copy followed by paste.

The microphone settings may need adjustment for your room and microphone. Use `--high` and `--low` to change the volume thresholds. The program uses NumPy for RMS because Python 3.13 no longer includes the older audioop module.

## Try it

Use Python 3.11 or newer. Open a terminal in this project's folder and create a virtual environment. This keeps its packages separate from your other Python projects.

```sh
python -m venv .venv
```

On Windows, activate it with this command.

```sh
.venv\Scripts\activate
```

On macOS or Linux, use this command instead.

```sh
source .venv/bin/activate
```

Then install the packages the project needs.

```sh
python -m pip install -r requirements.txt
```

```sh
python tap_macros.py --replay sample_taps.json
```

For microphone use, install the extra packages first.

```sh
python -m pip install -r requirements-live.txt
python tap_macros.py
python tap_macros.py --execute
```

Use `--device` to choose a microphone by its device number. PyAudio needs PortAudio, so some Linux systems also need the PortAudio development package.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests check two taps, three taps, long sounds, idle resets, and volume calculations. Microphone sensitivity still needs to be checked with your own setup.
