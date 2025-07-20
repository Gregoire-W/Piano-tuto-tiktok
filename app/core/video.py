from app.core.screen import Screen
from app.core.piano import Piano
from app.core.partition import Partition
from pathlib import Path
import cv2
from tqdm import tqdm
import numpy as np

class Video:

    def __init__(self, screen: Screen, piano: Piano, fps: int) -> None:
        self.fps = fps
        self.screen = screen
        self.piano = piano

    def generate(self, partition: Partition, output_path: Path) -> None:
        vid_format = self.screen.shape[:2]
        video = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), self.fps, vid_format[::-1])

        video_end = partition.notes[-1][0].end
        
        step = round(1 / self.fps, 2)
        times = []
        for i in range(int(video_end) + 1):
            times.extend(np.round(np.linspace(0, 1 - step, 30), 2) + i)

        for time in tqdm(times):
            time = round(time, 2)
            #input(f"time: {time}, next start: {partition.play_notes[-1][1]}, next stop: {partition.stop_notes[-1][1]}")

            for i in range(len(partition.play_notes)):
                pitch, start, instrument = partition.play_notes[-1]
                if start == time:
                    pitch -= 21
                    color = (255, 255, 0)
                    self.piano.press(pitch, color)
                    partition.play_notes.pop()
                else:
                    break

            for i in range(len(partition.stop_notes)):
                pitch, end, instrument = partition.stop_notes[-1]
                if end == time:
                    pitch -= 21
                    self.piano.release(pitch)
                    partition.stop_notes.pop()
                else:
                    break

            frame = self.screen.draw(self.piano.image, pos=self.screen.pos_img_bottom)
            video.write(frame)

        video.release()
        cv2.destroyAllWindows()
