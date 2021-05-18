import argparse
import os

import cv2
import numpy as np
import pyzed.sl as sl

from utilities import progress_bar

def export_png(svo_file: str, output_dir: str, start_frame: int, \
    stop_frame: int, skip_frame: int):
    assert os.path.exists(svo_file), "Input file does not exist."
    assert os.path.splitext(svo_file)[-1] == ".svo", \
        "Input file is not a SVO file."
    assert output_dir[-1] == '/', "Output directory must end with '/'."

    left_dir = output_dir + "Left/"
    right_dir = output_dir + "Right/"

    if not os.path.isdir(left_dir):
        os.mkdir(left_dir)

    if not os.path.isdir(right_dir):
        os.mkdir(right_dir)
   
    init_params = sl.InitParameters()
    init_params.set_from_svo_file(svo_file)
    init_params.svo_real_time_mode = False

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
        stop_frame = frames_total

    # Allocate.
    left_image = sl.Mat()
    right_image = sl.Mat()

    print()
    print("Export from: {0}".format(svo_file))
    print("Export to:   {0}".format(output_dir))
    print("Frames:      {0}-{1}".format(start_frame, stop_frame))

    running = True
    frame = 0
    while frame <= stop_frame and frame < frames_total:
        if zed.grab() != sl.ERROR_CODE.SUCCESS:
            continue

        frame = zed.get_svo_position()

        if (frame - start_frame) % skip_frame != 0:
            continue

        # Show progress bar.
        progress_bar((frame - start_frame) / (stop_frame - start_frame) * 100)

        # Get SVO images and timestamp.
        zed.retrieve_image(left_image, sl.VIEW.LEFT_UNRECTIFIED)
        zed.retrieve_image(right_image, sl.VIEW.RIGHT_UNRECTIFIED)
        timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)

        # Get RGB images.
        left_array = left_image.get_data()[:, :, :3]
        right_array = right_image.get_data()[:, :, :3]

        # Save images.
        cv2.imwrite("{0}{1}.png".format(left_dir, \
            timestamp.get_milliseconds()), left_array)
        cv2.imwrite("{0}{1}.png".format(right_dir, \
            timestamp.get_milliseconds()), right_array)

def main():
    parser = argparse.ArgumentParser(description="Export the images from a \
        SVO file as PNG files.")
    parser.add_argument("--input", type=str, help="Input SVO file.")
    parser.add_argument("--output", type=str, help="Output directory.")
    parser.add_argument("--start", type=int, help="Start index.")
    parser.add_argument("--stop", type=int, help="Stop index.")
    parser.add_argument("--skip", type=int, help="Index skip.")
    args = parser.parse_args()

    export_png(args.input, args.output, args.start, args.stop, args.skip)

if __name__ == "__main__":
    main()
