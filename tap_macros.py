import argparse
import json
import math
import time
from dataclasses import dataclass, field
import numpy as np

def rms(data):
    values = np.frombuffer(data, dtype='<i2').astype(float)
    return float(np.sqrt(np.mean(values**2))) if len(values) else 0.0

@dataclass
class TapDetector:
    high: float = 3000
    low: float = 1000
    gap: float = 0.8
    reset: float = 1.5
    taps: list = field(default_factory=list)
    ready: bool = True

    def __post_init__(self):
        if not all(math.isfinite(v) for v in (self.high,self.low,self.gap,self.reset)):
            raise ValueError('Thresholds and timing must be finite')
        if not 0 <= self.low < self.high or not 0 < self.gap <= self.reset:
            raise ValueError('Require 0 <= low < high and 0 < gap <= reset')

    def update(self, volume, now):
        action = None
        if self.taps and now - self.taps[-1] >= self.reset:
            self.taps.clear()
        elif self.taps and now - self.taps[-1] >= self.gap:
            action = {2:'copy',3:'paste'}.get(len(self.taps))
            self.taps.clear()
        if volume <= self.low:
            self.ready = True
        if self.ready and volume > self.high:
            self.taps.append(now)
            self.ready = False
        return action

def replay(events, detector=None):
    detector = detector or TapDetector()
    last = -float('inf')
    actions = []
    for now, volume in events:
        if not math.isfinite(now) or not math.isfinite(volume) or now < last or volume < 0:
            raise ValueError('Replay needs increasing finite times and nonnegative RMS values')
        last = now
        if action := detector.update(volume, now):
            actions.append(action)
    if events:
        if action := detector.update(0, last + detector.gap + 0.001):
            actions.append(action)
    return actions

def listen(detector, execute=False, device=None):
    import pyaudio
    if execute:
        import pyautogui
    audio = pyaudio.PyAudio()
    stream = None
    try:
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                            input_device_index=device, frames_per_buffer=1024)
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            if action := detector.update(rms(data), time.monotonic()):
                print(action, flush=True)
                if execute:
                    pyautogui.hotkey('ctrl', 'c' if action == 'copy' else 'v')
    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        audio.terminate()

def main():
    parser = argparse.ArgumentParser(description='Copy or paste with groups of microphone taps')
    parser.add_argument('--replay', help='JSON pairs of [seconds, RMS]')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--device', type=int)
    parser.add_argument('--high', type=float, default=3000)
    parser.add_argument('--low', type=float, default=1000)
    args = parser.parse_args()
    detector = TapDetector(high=args.high, low=args.low)
    if args.replay:
        with open(args.replay) as source:
            print(json.dumps(replay(json.load(source), detector)))
    else:
        try:
            listen(detector, args.execute, args.device)
        except KeyboardInterrupt:
            print('Stopped listening')

if __name__ == '__main__':
    main()
