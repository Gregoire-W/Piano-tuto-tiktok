from pathlib import Path
from app.core.partition import Partition
import numpy as np
from scipy.io import wavfile

class Instrument:

    def __init__(self, sf2_path: Path, type: str) -> None:
        self.sf2_path = sf2_path
        self.type = type

    def midi_to_wav(self, partition: Partition, output_path: Path) -> None:

        audio_data = partition.partition.fluidsynth(fs=44100, sf2_path=str(self.sf2_path))

        # Normalisation
        if np.max(np.abs(audio_data)) > 0:
            audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8

        # Conversion en entiers 16-bit
        audio_data_int = (audio_data * 32767).astype(np.int16)

        wavfile.write(str(output_path), 44100, audio_data_int)