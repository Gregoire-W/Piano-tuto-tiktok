from app.core.screen import Screen
from app.core.piano import Piano
from app.core.partition import Partition
from pathlib import Path
import cv2
from tqdm import tqdm
import numpy as np
import copy
import heapq
import itertools
from app.utils import compute_note_height

class Video:

    def __init__(self, screen: Screen, piano: Piano, fps: int) -> None:
        self.fps = fps
        self.screen = screen
        self.piano = piano

    def generate(self, partition: Partition, output_path: Path, img_coordinates: dict, timing: float) -> None:
        piano_pos = (0, img_coordinates["bottom"])

        vid_format = self.screen.shape[:2]
        video = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), self.fps, vid_format[::-1])
        video_end = partition.stop_notes[0][1]

        video_notes = copy.deepcopy(partition.notes)
        
        moving_notes = []
        playing_notes = []
        counter = itertools.count()

        step = round(1 / self.fps, 2)
        times = []
        for i in range(int(video_end) + 1):
            times.extend(np.round(np.linspace(0, 1 - step, 30), 2) + i)

        for time in tqdm(times):
            time = round(time, 2)
            #input(f"time: {time}, next start: {partition.play_notes[-1][1]}, next stop: {partition.stop_notes[-1][1]}")
            #input(f"time: {time}, playing_notes: {playing_notes}")

            self.draw_notes(video_notes, moving_notes, time, timing)
            self.play_notes(moving_notes, playing_notes, time, counter)
            self.release_notes(playing_notes, time)

            frame = self.screen.draw(self.piano.image, pos=piano_pos)
            video.write(frame)

        video.release()
        cv2.destroyAllWindows()

    def draw_notes(self, video_notes: list, moving_notes: list, time: float, timing: float) -> None:
        for i in range(len(video_notes)):
            note, instrument = video_notes[-1]
            if note.start - timing <= time:
                moving_notes.append(video_notes.pop())
            else:
                break
        self.draw_on_screen(moving_notes, time, timing)

    def play_notes(self, moving_notes: list, playing_notes: list, time: float, counter: itertools.count) -> None:
        # Check for all notes that should be played
        for i in range(len(moving_notes)): 
            note, instrument = moving_notes[0]
            if note.start == time:
                color = (255, 255, 0)
                self.piano.press(note.pitch - 21, color)
                
                note, instrument = moving_notes.pop(0)
                heapq.heappush(playing_notes, (note.end, next(counter), (note, instrument)))
            else:
                break

    def release_notes(self, playing_notes: list, time: float) -> None:
        for i in range(len(playing_notes)): 
            note, instrument = playing_notes[0][2]
            if note.end == time:
                self.piano.release(note.pitch - 21)
                heapq.heappop(playing_notes)

    def draw_on_screen(self, moving_notes: list, time: float, timing: float) -> None:
        for note, instrument in moving_notes:
            input(f"note: {type(note)}")
            x,  color, _ = self.piano.dict_tiles[note.pitch-21]
            width = self.piano.white_tile_width if color == (255, 255, 255) else self.piano.black_tile_width

            y = compute_note_height(note, time, timing)