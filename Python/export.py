import enum
import os
import sys

from typing import Tuple

import cv2
import numpy as np
import pyzed.sl as sl

from utilities import progress_bar

def export_png(svo_file: str, output_dir: str, start_frame: int, \
    stop_frame: int, skip_frame: int, offset: int, stereo: bool, \
    grayscale: bool, rectify: bool, preprocess: bool):
    assert os.path.exists(svo_file), "Input file does not exist."
    assert os.path.splitext(svo_file)[-1] == ".svo", \
        "Input file is not a SVO file."

    # BLF parameters.
    blf_radius = 7
    blf_sigmar = 20
    blf_sigmas = 20

    if stereo:
        left_dir = output_dir + "Left"
        right_dir = output_dir + "Right"
    else:
        left_dir = output_dir
        right_dir = output_dir

    if not os.path.isdir(left_dir):
        os.mkdir(left_dir)

    if not os.path.isdir(right_dir):
        os.mkdir(right_dir)

    if grayscale and rectify:
        left_image_type = sl.VIEW.LEFT_GRAY
        right_image_type = sl.VIEW.RIGHT_GRAY
    elif grayscale and not rectify:
        left_image_type = sl.VIEW.LEFT_UNRECTIFIED_GRAY
        right_image_type = sl.VIEW.RIGHT_UNRECTIFIED_GRAY
    elif not grayscale and rectify:
        left_image_type = sl.VIEW.LEFT
        right_image_type = sl.VIEW.RIGHT
    elif not grayscale and not rectify:
        left_image_type = sl.VIEW.LEFT_UNRECTIFIED
        right_image_type = sl.VIEW.RIGHT_UNRECTIFIED

    init_params = sl.InitParameters()
    init_params.set_from_svo_file(svo_file)
    init_params.svo_real_time_mode = False
    
    # Load SVO file.
    zed = sl.Camera()
    error = zed.open(init_params)
    if not error is sl.ERROR_CODE.SUCCESS:
        sys.std.write(repr(error))
        zed.close()
        exit()

    # Get SVO information and set SVO position.
    camera_info = zed.get_camera_information()
    frames_total = zed.get_svo_number_of_frames()
    zed.set_svo_position(start_frame)

    if stop_frame > frames_total:
        stop_frame = frames_total - 1

    # Allocate.
    left_image = sl.Mat()
    right_image = sl.Mat()

    print()
    print("Export from: {0}".format(svo_file))
    print("Export to:   {0}".format(output_dir))
    print("Frames:      {0}-{1}".format(start_frame, stop_frame))

    running = True
    frame = 0
    timestamps = []
    while frame < stop_frame-1 and frame < frames_total-1:
        if zed.grab() != sl.ERROR_CODE.SUCCESS:
            continue

        frame = zed.get_svo_position()
        index = frame + offset

        if (frame - start_frame) % skip_frame != 0:
            continue

        # Show progress bar.
        progress_bar((frame - start_frame) / (stop_frame - start_frame) * 100)

        # Get timestamp.
        timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
        timestamps.append((index, timestamp.get_milliseconds()))

        # Get the left image.
        zed.retrieve_image(left_image, left_image_type)
        left_array = left_image.get_data()
        if preprocess:
            left = cv2.bilateralFilter(left_array, blf_radius, \
                blf_sigmar, blf_sigmas)
        else:
            left = left_array
        cv2.imwrite("{0}/{1}.png".format(left_dir, index), left)

        # If stereo, get the right image.
        if stereo:
            zed.retrieve_image(right_image, right_image_type)
            right_array = right_image.get_data()
            if preprocess:
                right = cv2.bilateralFilter(right_array, blf_radius, \
                    blf_sigmar, blf_sigmas)
            else:
                right = right_array
            cv2.imwrite("{0}/{1}.png".format(right_dir, index), right)    

    # Save times to .txt file.
    with open(output_dir + "/Timestamps.txt", "w") as f:
        f.write("{0}, {1}\n".format("Index", "Timestamp"))
        for index, timestamp in timestamps:
            f.write("{0}, {1}\n".format(index, timestamp))


class SVOInspector(object):
    def __init__(self, svo_file: str, output_dir: str, start_frame: int, \
        bias: float=0, save_right: bool=False, \
        display_size: Tuple[int, int]=(1600, 900)):
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
        self.bias = bias
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

            time = ((timestamp.get_milliseconds() / 1000) + self.bias) * 1000

            if capturing:
                cv2.imwrite("{0}{1}-left.png".format(self.output_dir, time), \
                    left_array)
            if capturing and self.save_right:
                cv2.imwrite("{0}{1}-right.png".format(self.output_dir, time), \
                    right_array)

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
