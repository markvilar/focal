from enum import Enum

class FrameType(Enum):
    GREY = 1
    RGB = 2
    DISPARITY = 3
    DEPTH = 4

class ImageFileFormat(Enum):
    JPEG = 1
    PNG = 2
    TIFF = 3

