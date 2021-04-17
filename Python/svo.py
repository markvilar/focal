import enum
import os
import sys

from typing import Tuple

import cv2
import numpy as np
import pyzed.sl as sl

from utilities import progress_bar

class SVOInspector(object):
    def __init__(self, svo_file: str, output_dir: str, start_frame: int,
        save_right: bool=False, display_size: Tuple[int, int]=(1600, 900)):
        assert os.path.exists(svo_file), \
            "Input file does not exist."
        assert os.path.splitext(svo_file)[-1] == ".svo", \
            "Input file is not a SVO file."
        assert output_dir[-1] == '/', \
            "Output directory must end with '/'."
        assert start_frame >= 0, "Start index must be zero or larger."
		
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
		
        self.svo_file = svo_file
        self.output_dir = output_dir
        self.start_frame = start_frame
        self.save_right = save_right
        self.display_size = display_size

        self.camera_info = None

        self.init_params = sl.InitParameters()
        self.init_params.set_from_svo_file(self.svo_file)
        self.init_params.svo_real_time_mode = False
        self.init_params.coordinate_units = sl.UNIT.MILLIMETER

    def inspect(self):
        # Open SVO.
        zed = sl.Camera()
        error = zed.open(self.init_params)
        if not error is sl.ERROR_CODE.SUCCESS:
            sys.std.write(repr(error))
            zed.close()
            exit()

        # Get SVO information and set SVO position.
        self.camera_info = zed.get_camera_information()
        total_frames = zed.get_svo_number_of_frames()
        if self.start_frame < total_frames:
            zed.set_svo_position(self.start_frame)

		# Calculate size and scale.
        stereo_width = 2 * self.camera_info.camera_resolution.width
        stereo_height = self.camera_info.camera_resolution.height
        aspect_ratio = stereo_width / stereo_height
        scale = min(float(self.display_size[0] / stereo_width), 
            float(self.display_size[1] / stereo_height))
        new_size = (int(scale * stereo_width), 
            int(scale * stereo_height))
		
        # Allocate.
        left_image = sl.Mat()
        right_image = sl.Mat()

        capturing = False
        running = True
        while running:
            if zed.grab() != sl.ERROR_CODE.SUCCESS:
                continue

            frame = zed.get_svo_position()

            # Get SVO images and timestamp.
            zed.retrieve_image(left_image, sl.VIEW.LEFT_UNRECTIFIED)
            zed.retrieve_image(right_image, sl.VIEW.RIGHT_UNRECTIFIED)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)

            # Get images.
            left_array = left_image.get_data()
            right_array = right_image.get_data()

            # Concatenate images.
            stereo_array = np.concatenate((left_array, right_array),
                axis=1)

            # Resize stereo image to fit on screen.
            stereo_array = cv2.resize(stereo_array, new_size)

            # Display image.
            cv2.imshow("Left | Right", stereo_array)

            if capturing:
                cv2.imwrite("{0}{1}-left.png".format(self.output_dir, 
                    timestamp.get_milliseconds()), left_array)
            if capturing and self.save_right:
                cv2.imwrite("{0}{1}-right.png".format(self.output_dir, 
                    timestamp.get_milliseconds()), right_array)

            key_code = cv2.waitKey(int(1000/self.camera_info.camera_fps))

            if key_code == 32: # Spacebar
                capturing = not capturing
                if capturing:
                    sys.stdout.write("Saving images...\n")
                    sys.stdout.flush()
                else:
                    sys.stdout.write("Stopped saving images...\n")
                    sys.stdout.flush()
            elif key_code == 27 or frame == total_frames:
                running = False
            elif key_code == -1:
                continue
			
        cv2.destroyAllWindows()

class Format(enum.Enum):
    Default = 1

def format_from_string(string: str) -> Format:
    if string == "Default":
        return Format.Default
    else:
        return None
