import numpy as np

class Screen:

    def __init__(self, background: np.ndarray, img_bottom: int) -> None:
        self.background = background
        self.shape = background.shape
        self.display_img = np.copy(background)
        self.pos_img_bottom = (0, img_bottom)

    def draw(self, image: np.ndarray, pos: tuple) -> np.ndarray:
        x, y = pos
        h, w, c = image.shape
        self.display_img[y:y+h, x:x+w] = image
        return self.display_img

    def reset(self) -> None:
        self.display_img = np.copy(self.background)
    