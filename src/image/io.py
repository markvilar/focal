from pathlib import Path

import cv2
import numpy as np

def save_image(image: np.ndarray, path: Path):
    """ """
    cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, 100])
