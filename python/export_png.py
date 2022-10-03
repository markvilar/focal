import argparse
import os

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
    blf_radius = 10
    blf_sigmar = 60
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

def main():
    parser = argparse.ArgumentParser(description="Export the images from a \
        SVO file as PNG files.")
    parser.add_argument("--input", type=str, \
        help="Input SVO file.")
    parser.add_argument("--output", type=str, \
        help="Output directory.")
    parser.add_argument("--start", type=int, \
        help="Start index.")
    parser.add_argument("--stop", type=int, \
        help="Stop index.")
    parser.add_argument("--skip", type=int, \
        help="Index skip.")
    parser.add_argument("--offset", type=int, default=0, \
        help="Frame index offset.")
    parser.add_argument("--stereo", type=bool, default=False, \
        help="Extract stereo images.")
    parser.add_argument("--grayscale", type=bool, default=True, \
        help="Extract grayscale images.")
    parser.add_argument("--rectify", type=bool, default=True, \
        help="Rectify images.")
    parser.add_argument("--preprocess", type=bool, default=True, \
        help="Preprocess images.")
    args = parser.parse_args()

    export_png(args.input, args.output, args.start, args.stop, args.skip, \
        args.offset, args.stereo, args.grayscale, args.rectify, \
        args.preprocess)

if __name__ == "__main__":
    main()
