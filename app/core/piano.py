import numpy as np
from app.utils import get_tile
import cv2

class Piano:

    def __init__(self, width: int, white_tile_height: int, sep_size: int) -> None:
        assert sep_size % 2 == 0, "sep_size attributes in Piano class must be an even number"
        self.width = width
        self.left_px = self.width % 52
        self.white_tile_width = self.width // 52 - sep_size
        self.black_tile_width = int(self.white_tile_width * (3/4))
        self.black_tile_width = self.black_tile_width + 1 if self.black_tile_width % 2 != 0 else self.black_tile_width # make it even number
        self.white_tile_height = white_tile_height
        self.black_tile_height = int((6/10) * self.white_tile_height)
        self.sep_size = sep_size
        self.dict_tiles = {}
        self.image = self.init_image()

    def add_white_tiles(self, image, num_white_tiles):
        start = self.left_px // 2 + 1
        dict_count = 0
        for count, (tile_number, tyle_type) in enumerate(zip(num_white_tiles[:2], [2, 3])):
            points = self.get_tile(tyle_type, (start, 0))
            cv2.fillPoly(image, [points], (255, 255, 255))
            start += self.white_tile_width+self.sep_size
            self.dict_tiles[tile_number] = (start,  (255, 255, 255), points)

        # Use a mapping to know for each pos what's the corresponding tile type
        map_pos_type = {i: k for i, k in zip(range(7), [2, 1, 3, 2, 1, 1, 3])}
        for count, tile_number in enumerate(num_white_tiles[2:-1], start = 2):
            tile_pos = (count - 2) % 7
            tyle_type = map_pos_type[tile_pos]
            points = self.get_tile(tyle_type, (start, 0))
            cv2.fillPoly(image, [points], (255, 255, 255))
            self.dict_tiles[tile_number] = (start,  (255, 255, 255), points)
            start += self.white_tile_width + self.sep_size

        # Add last tile
        points = self.get_tile(0, (start, 0))
        cv2.fillPoly(image, [points], (255, 255, 255))
        self.dict_tiles[num_white_tiles[-1]] = (start,  (255, 255, 255), points)

        return image

    def add_black_tiles(self, image, num_black_tiles):
        start = self.left_px // 2 + self.white_tile_width + (self.sep_size // 2) - (self.black_tile_width // 2) + 1 # +1 for the same reason as above
        points = self.get_tile(4, (start, 0)) # Type 4 is for black tiles
        cv2.fillPoly(image, [points], (0, 0, 0))
        self.dict_tiles[num_black_tiles[0]] = (start,  (0, 0, 0), points)
        for block in range(7):
            for i in range(5):
                if i in [0, 2]:
                    start += 2*(self.white_tile_width + self.sep_size)
                else:
                    start += self.white_tile_width + self.sep_size
                points = self.get_tile(4, (start, 0)) # Type 4 is for black tiles
                cv2.fillPoly(image, [points], (0, 0, 0))
                tile_number = num_black_tiles[block*5 + i + 1] # +1 bc we already put the first tile before
                self.dict_tiles[tile_number] = (start,  (0, 0, 0), points)
        return image

    def init_image(self) -> np.ndarray:
        image = np.zeros((self.white_tile_height, self.width, 3))

        num_black_tiles = [1] + [elem + 12*j for elem in [4, 6, 9, 11, 13] for j in range(7)]
        num_black_tiles.sort()
        num_white_tiles = [i for i in range(88) if i not in num_black_tiles]

        image = self.add_white_tiles(image, num_white_tiles)
        image = self.add_black_tiles(image, num_black_tiles)

        return image

    def press(self, note: int, color: tuple) -> None:
        x, tile_color, points = self.dict_tiles[note]
        cv2.fillPoly(self.image, [points], color)

    def release(self, note: int) -> None:
        x, tile_color, points = self.dict_tiles[note]
        cv2.fillPoly(self.image, [points], tile_color)

    def get_tile(self, tile_type: str, pos: tuple) -> np.array:
        x_short, y_short = pos
        y_mid = y_short + self.black_tile_height
        y_long = y_short + self.white_tile_height - 1
        x_long = x_short + self.white_tile_width - 1
        x_mid_1 = x_long + self.sep_size//2 - self.black_tile_width//2
        x_mid_2 = x_short - self.sep_size//2 + self.black_tile_width//2

        if tile_type == 0:
            points = np.array([[x_short, y_short], [x_short, y_long], [x_long, y_long], [x_long, y_short],])
        elif tile_type == 1:
            points = np.array([
                [x_mid_2, y_short], [x_mid_2, y_mid], [x_short, y_mid], [x_short, y_long],
                [x_long, y_long], [x_long, y_mid], [x_mid_1, y_mid], [x_mid_1, y_short],
            ])
        elif tile_type == 2:
            points = np.array([
                [x_short, y_short], [x_short, y_long], [x_long, y_long], [x_long, y_mid],
                [x_mid_1, y_mid], [x_mid_1, y_short],
            ])
        elif tile_type == 3:
            points = np.array([
                [x_mid_2, y_short], [x_mid_2, y_mid], [x_short, y_mid], [x_short, y_long],
                [x_long, y_long], [x_long, y_short],
            ])
        elif tile_type == 4:
            points = np.array([[x_short, y_short], [x_short, y_mid - 1], [x_short + self.black_tile_width - 1, y_mid - 1], [x_short + self.black_tile_width - 1, y_short],])
        else:
            raise ValueError(f"tile_type must be in [1, 2, 3, 4, 5] | your value: tile_type={tile_type}")
        points = points.reshape((-1, 1, 2))

        return points
