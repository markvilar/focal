import enum
import os
import sys

from pathlib import Path

from typing import Tuple

import arrow
import cv2
import numpy as np
import pyzed.sl as sl

class SVOInspector(object):
    def __init__(self, svo_file: str, output_dir: str, start_frame: int, \
        offset: float=0, display_size: Tuple[int, int]=(1600, 900)):
        assert os.path.exists(svo_file), \
            "Input file does not exist."
        assert os.path.splitext(svo_file)[-1] == ".svo", \
            "Input file is not a SVO file."
        assert output_dir[-1] == '/', \
            "Output directory must end with '/'."
        assert start_frame >= 0, "Start index must be zero or larger."
		
        output_dir = Path(output_dir)
        left_dir = output_dir / "left"
        right_dir = output_dir / "right"

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if not os.path.exists(left_dir):
            os.mkdir(left_dir)
        if not os.path.exists(right_dir):
            os.mkdir(right_dir)

        self.output_dir = output_dir
        self.left_dir = left_dir
        self.right_dir = right_dir

        self.display_fps = 30

        self.svo_file = svo_file
        self.start_frame = start_frame
        self.offset = offset
        self.display_size = display_size

        self.camera_info = None

        self.init_params = sl.InitParameters()
        self.init_params.set_from_svo_file(self.svo_file)
        self.init_params.svo_real_time_mode = False

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
        total_frames = zed.get_svo_number_of_frames() - 1
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

        capture = False
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
            stereo_array = np.concatenate((left_array, right_array), axis=1)

            # Resize stereo image to fit on screen.
            stereo_array = cv2.resize(stereo_array, new_size)

            # Display image.
            cv2.imshow("Left | Right", stereo_array)
            
            # Create timestamp
            timestamp = float((timestamp.get_milliseconds() / 1000) 
                + self.offset)
            datetime = arrow.Arrow.fromtimestamp(timestamp)
            time_string = datetime.strftime("%Y%m%d_%H%M%S_%f")

            left_path = self.left_dir / Path(time_string + ".png")
            right_path = self.right_dir / Path(time_string + ".png")

            if capture:
                cv2.imwrite(str(left_path), left_array)
                cv2.imwrite(str(right_path), right_array)

            key_code = cv2.waitKey(int(1000 / self.display_fps))

            if key_code == 32: # Spacebar
                capture = True
                if capture:
                    sys.stdout.write("Saving image...\n")
                    sys.stdout.flush()
                else:
                    sys.stdout.write("Not saving image...\n")
                    sys.stdout.flush()
            elif key_code == 27 or frame == total_frames:
                running = False
            elif key_code == -1:
                capture = False
                continue
        cv2.destroyAllWindows()
