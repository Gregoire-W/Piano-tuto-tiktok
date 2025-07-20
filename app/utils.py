from pathlib import Path
import cv2
import numpy as np

def init_background(img_path: Path, height: int, width: int, img_format: tuple=(9, 8)) -> tuple:

    img = cv2.imread(str(img_path))
    h, w, c = img.shape

    scale_w = w / width
    scale_h = h / int((img_format[1] / img_format[0]) * width)
    if scale_w != 1 or scale_h != 1:
        if scale_w < scale_h:
            new_height = int(h / scale_w)
            img = cv2.resize(img, (width, new_height), interpolation=cv2.INTER_LINEAR)
        else:
            new_width = int(w / scale_h)
            img = cv2.resize(img, (new_width, int((img_format[1] / img_format[0]) * width)), interpolation=cv2.INTER_LINEAR)


    h, w, c = img.shape
    if h > (img_format[1] / img_format[0]) * w:
        new_h = int((img_format[1] / img_format[0]) * w)
        start = (h - new_h) // 2
        img = img[start:start+new_h, :]
    elif w > width:
        start = (w - width) // 2
        img = img[:, start:start+width]


    background = np.zeros((height, width, 3))
    height_background, width_background = background.shape[:2]
    height_img = img.shape[0]

    y_start = height_background // 2 - height_img // 2
    background[y_start:y_start+height_img, :] = img

    return background.astype(np.uint8), y_start+height_img

def get_tiles(white_tile_shape: tuple, black_tile_shape: tuple) -> list:
    w_height, w_width = white_tile_shape
    b_height, b_width = black_tile_shape
    tiles = [
        np.array([
            
        ]),
        np.array([

        ]),
        np.array([

        ]),
    ]
def get_tile(tile_type: str, pos: tuple, white_tile_shape: tuple, black_tile_shape: tuple, sep_size: int) -> np.array:
    white_h, white_w = white_tile_shape
    black_h, black_w = black_tile_shape
    x_short, y_short = pos
    y_mid = y_short + black_h
    y_long = y_short + white_h
    x_long = x_short + white_w
    x_mid_1 = x_short + (white_w - black_w)//2
    x_mid_2 = white_w - x_mid_1
    x_mid_3 = x_short + white_w + sep_size//2 - black_w//2
    x_mid_4 = x_short - sep_size//2 + black_w//2

    if tile_type == 1:
        points = np.array([[x_short, y_short], [x_short, y_long], [x_long, y_long], [x_long, y_short],])
    elif tile_type == 2:
        points = np.array([
            [x_short, y_short], [x_short, y_long], [x_long, y_long], [x_long, y_short],
            [x_mid_2, y_short], [x_mid_2, y_mid], [x_mid_1, y_mid], [x_mid_1, y_short],
        ])
    elif tile_type == 3:
        points = np.array([
            [x_short, y_short], [x_short, y_long], [x_long, y_long], [x_long, y_mid],
            [x_mid_3, y_mid], [x_mid_3, y_short],
        ])
    elif tile_type == 4:
        points = np.array([
            [x_mid_4, y_short], [x_mid_4, y_mid], [x_short, y_mid], [x_short, y_long],
            [x_long, y_long], [x_long, y_short],
        ])
    else:
        raise ValueError("tile_type must be in [1, 2, 3, 4]")
    points = points.reshape((-1, 1, 2))

    return points
