"""Layered sound mixer: one volume slider per audio file.

Drop .wav / .mp3 files into the `sounds/` folder next to this script,
run it, and every file plays on a loop with its own slider.
"""
import sys
import tkinter as tk
from pathlib import Path

import pygame

SOUNDS_DIR = Path(__file__).resolve().parent / "audio_files"
EXTENSIONS = {".wav", ".mp3"}
START_VOLUME = 0.5


def load_tracks():
    """Load every supported audio file in SOUNDS_DIR."""
    tracks = []
    for path in sorted(SOUNDS_DIR.iterdir()):
        if path.suffix.lower() not in EXTENSIONS:
            continue
        try:
            sound = pygame.mixer.Sound(str(path))
        except pygame.error as err:
            print(f"Skipping {path.name}: {err}")
            continue
        sound.set_volume(START_VOLUME)
        sound.play(loops=-1)  # loop forever
        tracks.append((path.stem, sound))
    return tracks


def main():
    SOUNDS_DIR.mkdir(exist_ok=True)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)  # room for many layers

    root = tk.Tk()
    root.title("Layered water_wind")

    tracks = load_tracks()
    if not tracks:
        tk.Label(
            root,
            text=f"No .wav or .mp3 files found in:\n{SOUNDS_DIR}",
            padx=20, pady=20,
        ).pack()
        root.mainloop()
        return

    for name, sound in tracks:
        frame = tk.Frame(root, padx=12, pady=6)
        frame.pack(fill="x")
        tk.Label(frame, text=name, anchor="w", width=24).pack(side="left")
        slider = tk.Scale(
            frame, from_=0, to=100, orient="horizontal", length=300,
            command=lambda v, s=sound: s.set_volume(int(v) / 100),
        )
        slider.set(int(START_VOLUME * 100))
        slider.pack(side="left")

    paused = tk.BooleanVar(value=False)

    def toggle_pause():
        if paused.get():
            pygame.mixer.unpause()
            button.config(text="Pause all")
        else:
            pygame.mixer.pause()
            button.config(text="Resume all")
        paused.set(not paused.get())

    button = tk.Button(root, text="Pause all", command=toggle_pause)
    button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: (pygame.mixer.quit(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    sys.exit(main())
