import os

from typing import Tuple

import numpy as np

try:
    import pyzed.sl as sl
except ImportError:
    print("Cannot import ZED SDK.")

class Dataloader():
    def __init__(self):
        """ """
        pass

    def is_loaded(self):
        """ """
        raise NotImplementedError

    def load(self):
        """ """
        raise NotImplementedError

    def has_image(self) -> bool:
        """ """
        raise NotImplementedError
        
    def get_frame(self) -> Tuple:
        """ """
        raise NotImplementedError

class SVODataloader(Dataloader):
    def __init__(self):
        """ """
        Dataloader.__init__(self)
        self._reset()

    def _reset(self):
        """ """
        self._loaded = False
        self._init_paramss = None
        self._handle = None
        self._frame_index = 0
        self._frame_num = 0

    def is_loaded(self):
        """ """
        return self._loaded

    def load(self, path):
        """ """
        self._path = path
        self._init_paramss = sl.InitParameters()
        self._init_paramss.set_from_svo_file(self._path)
        self._init_paramss.svo_real_time_mode = False
        self._handle = sl.Camera()

        error = self._handle.open(self._init_paramss)
        if not error is sl.ERROR_CODE.SUCCESS:
            sys.std.write(repr(error))
            self._handle.close()
            exit()

        self._loaded = True
        self._frame_num = self._handle.get_svo_number_of_frames()

    def has_image(self) -> bool:
        """ """
        return self._frame_index < self._frame_num

    def get_frame(self, rectify: bool=True, grayscale: bool=True) \
        -> Tuple[int, np.ndarray, np.ndarray]:
        """ """
        if grayscale and rectify:
            left_type = sl.VIEW.LEFT_GRAY
            right_type = sl.VIEW.RIGHT_GRAY
        elif grayscale and not rectify:
            left_type = sl.VIEW.LEFT_UNRECTIFIED_GRAY
            right_type = sl.VIEW.RIGHT_UNRECTIFIED_GRAY
        elif not grayscale and rectify:
            left_type = sl.VIEW.LEFT
            right_type = sl.VIEW.RIGHT
        elif not grayscale and not rectify:
            left_type = sl.VIEW.LEFT_UNRECTIFIED
            right_type = sl.VIEW.RIGHT_UNRECTIFIED

        left_mat = sl.Mat()
        right_mat = sl.Mat()

        if self._handle.grab() != sl.ERROR_CODE.SUCCESS:
            return ( None, None, None )
    
        self._frame_index = self._handle.get_svo_position()
        time = self._handle.get_timestamp(sl.TIME_REFERENCE.IMAGE)
        self._handle.retrieve_image(left_mat, left_type)
        self._handle.retrieve_image(right_mat, right_type)
        return ( time.get_milliseconds(), left_mat.get_data(), \
            right_mat.get_data() )

    def set_index(self, index: int):
        """ """
        assert self._loaded, "Data is not loaded."
        assert index >= 0, "Invalid index."
        self._handle.set_svo_position(index)
