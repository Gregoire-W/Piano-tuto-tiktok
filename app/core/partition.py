from pathlib import Path
import numpy as np
from pretty_midi import PrettyMIDI

class Partition:

    def __init__(self, partition_path: Path, fps: int):
        self.partition = PrettyMIDI(str(partition_path))
        self.notes = self.init_notes(self.partition, fps) 
        self.play_notes = [(note.pitch, note.start, instrument) for note, instrument in self.notes]
        self.play_notes = sorted(self.play_notes, key=lambda x: x[1], reverse=True)
        self.stop_notes = [(note.pitch, note.end, instrument) for note, instrument in self.notes]
        self.stop_notes = sorted(self.stop_notes, key=lambda x: x[1], reverse=True)


    def get_new_timing(self, timing: float, fps: int, step: float, rounded: np.array) -> float:

        dec_part = timing % 1
        return round(int(timing) + rounded[np.argmin(np.abs(rounded - dec_part))], 2)


    def adapt_to_fps(self, notes: list, fps: int) -> None:
        step = round(1 / fps, 2)
        rounded = np.linspace(0, 1 - step, 30)
        rounded = np.round(rounded, 2)
        for note, instrument in notes:
            note.start = self.get_new_timing(note.start, fps, step, rounded)
            note.end = self.get_new_timing(note.end, fps, step, rounded)
        return notes

    def init_notes(self, notes: list, fps: int) -> tuple:
        notes = [(note, instrument) for instrument in self.partition.instruments for note in instrument.notes]
        notes = self.adapt_to_fps(notes, fps)
        notes = sorted(notes, key=lambda x: x[0].start, reverse=True)
        return notes