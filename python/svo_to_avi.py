import sys
import pyzed.sl as sl
import numpy as np
import cv2
from pathlib import Path
import enum


class AppType(enum.Enum):
	LEFT_AND_RIGHT = 1
	LEFT_AND_DEPTH = 2
	LEFT_AND_DEPTH_16 = 3


def progress_bar(percent_done, bar_length=50):
	done_length = int(bar_length * percent_done / 100)
	bar = '=' * done_length + '-' * (bar_length - done_length)
	sys.stdout.write('[%s] %f%s\r' % (bar, percent_done, '%'))
	sys.stdout.flush()


def main():
	if not sys.argv or len(sys.argv) != 4:
		sys.stdout.write("Usage: \n\n")
		sys.stdout.write("    ZED_SVO_Export A B C \n\n")
		sys.stdout.write("Please use the following parameters from the \
			command line:\n")
		sys.stdout.write(" A - SVO file path (input) : \"path/to/file.svo\"\n")
		sys.stdout.write(" B - AVI file path (output) or image sequence \
			folder(output) :\n")
		sys.stdout.write("         \"path/to/output/file.avi\" or \
			\"path/to/output/folder\"\n")
		sys.stdout.write(" C - Export mode:  0=Export LEFT+RIGHT AVI.\n")
		sys.stdout.write("                   1=Export LEFT+DEPTH_VIEW AVI.\n")
		sys.stdout.write(" A and B need to end with '/' or '\\'\n\n")
		sys.stdout.write("Examples: \n")
		sys.stdout.write("  (AVI LEFT+RIGHT):  ZED_SVO_Export \
			\"path/to/file.svo\" \"path/to/output/file.avi\" 0\n")
		sys.stdout.write("  (AVI LEFT+DEPTH):  ZED_SVO_Export \
			\"path/to/file.svo\" \"path/to/output/file.avi\" 1\n")
		exit()

	# Get input parameters
	svo_input_path = Path(sys.argv[1])
	output_path = Path(sys.argv[2])
	output_as_video = True    
	app_type = AppType.LEFT_AND_RIGHT
	if sys.argv[3] == "1":
		app_type = AppType.LEFT_AND_DEPTH

	# Initialization parameters.
	init_params = sl.InitParameters()
	init_params.set_from_svo_file(str(svo_input_path))
	init_params.svo_real_time_mode = False
	init_params.coordinate_units = sl.UNIT.METER

	# Runtime parameters.
	rt_param = sl.RuntimeParameters()
	rt_param.sensing_mode = sl.SENSING_MODE.FILL

	# Create ZED objects.
	zed = sl.Camera()

	# Open the SVO file specified as a parameter.
	err = zed.open(init_params)
	if err != sl.ERROR_CODE.SUCCESS:
		sys.stdout.write(repr(err))
		zed.close()
		exit()

	# Get image size.
	image_size = zed.get_camera_information().camera_resolution
	width = image_size.width
	height = image_size.height
	width_sbs = width * 2

	# Prepare side by side image container equivalent to CV_8UC4.
	svo_image_sbs_rgba = np.zeros((height, width_sbs, 4), dtype=np.uint8)

	# Prepare single image containers.
	left_image = sl.Mat()
	right_image = sl.Mat()
	depth_image = sl.Mat()

	# Extract SVO timestamps.
	frames_total = zed.get_svo_number_of_frames()
	timestamp_start, timestamp_end = None, None

	if zed.grab() == sl.ERROR_CODE.SUCCESS:
		timestamp_start = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)

	zed.set_svo_position(frames_total - 1)

	if zed.grab() == sl.ERROR_CODE.SUCCESS:
		timestamp_end = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)

	# Calculate effective FPS.
	duration = (timestamp_end.get_milliseconds() - \
		timestamp_start.get_milliseconds()) / 1000
	fps = frames_total / duration

	print("Target FPS: {0}".format(fps))

	# Create video writer with MPEG-4 part 2 codec.
	video_writer = cv2.VideoWriter(str(output_path), 
		cv2.VideoWriter_fourcc('M', '4', 'S', '2'), fps, 
		(width_sbs, height))

	if not video_writer.isOpened():
		sys.stdout.write("OpenCV video writer cannot be opened. Please check \
			the .avi file path and write permissions.\n")
		zed.close()
		exit()

	# Start SVO conversion to AVI.
	sys.stdout.write("Converting SVO... Use Ctrl-C to interrupt conversion.\n")

	# Set SVO position to start.
	zed.set_svo_position(0)

	# Extract images.
	while True:
		if zed.grab(rt_param) == sl.ERROR_CODE.SUCCESS:
			# Retrieve SVO images.
			zed.retrieve_image(left_image, sl.VIEW.LEFT)
			if app_type == AppType.LEFT_AND_RIGHT:
				zed.retrieve_image(right_image, sl.VIEW.RIGHT)
			elif app_type == AppType.LEFT_AND_DEPTH:
				zed.retrieve_image(right_image, sl.VIEW.DEPTH)
			elif app_type == AppType.LEFT_AND_DEPTH_16:
				zed.retrieve_measure(depth_image, sl.MEASURE.DEPTH)

			# Create side by side image.
			svo_image_sbs_rgba[0:height, 0:width, :] = left_image.get_data()
			svo_image_sbs_rgba[0:, width:, :] = right_image.get_data()

			# Convert SVO image from RGBA to RGB.
			ocv_image_sbs_rgb = cv2.cvtColor(svo_image_sbs_rgba, 
				cv2.COLOR_RGBA2RGB)

			# Write the RGB image in the video.
			video_writer.write(ocv_image_sbs_rgb)
			
			# Get SVO position and display progress.
			svo_position = zed.get_svo_position()
			progress_bar((svo_position + 1) / frames_total * 100, 30)

			# Check if we have reached the end of the video.
			if svo_position >= (frames_total - 1): 
				sys.stdout.write("\nSVO end has been reached. Exiting now.\n")
				break

	# Close the video writer
	video_writer.release()

	zed.close()
	return 0


if __name__ == "__main__":
	main()
