import os

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import arrow
import numpy as np

try:
    import pyzed.sl as sl
except ImportError:
    print("Cannot import ZED SDK.")


@dataclass
class FrameLoader():
    filepath: Path
    parameters: sl.InitParameters=sl.InitParameters()
    camera: sl.Camera=sl.Camera()
    index: int=0
    step: int=1
    count: int=0

    def __post_init__(self):
        self.parameters.set_from_svo_file(str(self.filepath))

    def prepare(self):
        status = self.camera.open(self.parameters)
        if not status is sl.ERROR_CODE.SUCCESS:
            sys.std.write(repr(status))
            self.camera.close()
            exit()
        self.camera.set_svo_position(self.index)
        self.count = self.camera.get_svo_number_of_frames()

    def load_frame(self):
        left_mat = sl.Mat()
        right_mat = sl.Mat()

        if self.camera.grab() != sl.ERROR_CODE.SUCCESS:
            return ( None, None, None )
        
        self.index = self.camera.get_svo_position()
        time = self.camera.get_timestamp(sl.TIME_REFERENCE.IMAGE)
        self.camera.retrieve_image(left_mat, sl.VIEW.LEFT_UNRECTIFIED)
        self.camera.retrieve_image(right_mat, sl.VIEW.RIGHT_UNRECTIFIED)
       
        timestamp = arrow.get(time.get_milliseconds())
        left_image = left_mat.get_data()
        right_image = right_mat.get_data()
        
        return ( timestamp, left_image, right_image )
