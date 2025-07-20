from pathlib import Path
from app.core.screen import Screen
from app.core.partition import Partition
from app.core.piano import Piano
from app.utils import init_background
from app.core.video import Video
from app.core.sound import Instrument
import subprocess

def main(
    img_path: Path,
    partition_path: Path,
    height: int,
    width: int,
    output_dir: Path,
    fps: int,
    sf2_path: Path,
):
    background, img_bottom = init_background(img_path, height, width)
    screen = Screen(background, img_bottom)
    partition = Partition(partition_path, fps=fps)
    piano = Piano(width=width, white_tile_height=55, sep_size=2)
    video = Video(screen, piano, fps=fps)

    video_path = output_dir / "video.mp4"
    video.generate(partition, str(video_path))
    print(f"\033[92mVideo released successfuly: {str(video_path)}\033[0m")

    audio_path = Path(output_dir / "audio.wav")
    instrument = Instrument(sf2_path, "piano")
    instrument.midi_to_wav(partition, audio_path)
    print(f"\033[92mAudio released successfuly: {str(audio_path)}\033[0m")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),    # Input 0
        "-i", str(audio_path),    # Input 1
        "-map", "0:v:0",          # Prendre la vidéo du premier input
        "-map", "1:a:0",          # Prendre l'audio du second input
        "-c:v", "copy",           # Copier la vidéo sans réencodage
        "-c:a", "aac",            # Encoder l'audio en AAC
        "-shortest",
        "output.mp4",
    ]

    subprocess.run(cmd)
