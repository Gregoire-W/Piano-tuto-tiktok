from pathlib import Path
import cv2
import numpy as np

def init_background(img_path: Path, height: int, width: int, img_format: tuple=(9, 8)) -> np.array:

    img = cv2.imread(str(img_path))
    h, w, c = img.shape

    scale_w = w / width

    if scale_w != 1:
        img = cv2.resize(img, (int(w/scale_w), int(h/scale_w)), interpolation=cv2.INTER_LINEAR)

    if h > height:
        y_crop = h // 2 - height // 2
        img = img[y_crop:+y_crop+h, :]

    background = np.zeros((height, width, 3))
    height_background, width_background = background.shape[:2]
    height_img = img.shape[0]

    y_start = height_background // 2 - height_img // 2
    background[y_start:y_start+height_img, :] = img

    return background.astype(np.uint8), {"top": y_start, "bottom": y_start+height_img}

def compute_note_height(note: float, time: float, timing: float) -> int:
    pass
