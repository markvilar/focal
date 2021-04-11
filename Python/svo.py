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
		display_size: Tuple[int, int]=(1600, 900)):
		assert os.path.exists(svo_file), \
			"Input file does not exist."
		assert os.path.splitext(svo_file)[-1] == ".svo", \
			"Input file is not a SVO file."
		assert output_dir[-1] == '/', \
			"Output directory must end with '/'."
		assert start_frame > 0, "Start index must be larger than zero."
		
		if not os.path.isdir(output_dir):
			os.mkdir(output_dir)
		
		self.svo_file = svo_file
		self.output_dir = output_dir
		self.start_frame = start_frame
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
			zed.retrieve_image(left_image, 
				sl.VIEW.LEFT_UNRECTIFIED)
			zed.retrieve_image(right_image,
				sl.VIEW.RIGHT_UNRECTIFIED)
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
				cv2.imwrite("{0}{1}-left.png".format(
					self.output_dir, 
					timestamp.get_milliseconds()), 
					left_array)
				cv2.imwrite("{0}{1}-right.png".format(
					self.output_dir, 
					timestamp.get_milliseconds()), 
					right_array)

			key_code = cv2.waitKey(
				int(1000/self.camera_info.camera_fps))

			if key_code == 32: # Spacebar
				capturing = not capturing
				if capturing:
					sys.stdout.write("Saving images...\n")
					sys.stdout.flush()
				else:
					sys.stdout.write("Stopped saving " \
						"images...\n")
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

class SVOFormatter:
	def __init__(self, svo_file: str, output_dir=None, fill=8):
		if not os.path.exists(svo_file):
			raise Exception('Input file does not exists.')
		if os.path.splitext(svo_file)[-1].lower() != ".svo":
			raise Exception('Input file is not a SVO file.')

		if output_dir != None:
			root = output_dir
		else:
			root = "".join(list(os.path.split(svo_file)[:-1]))

		self.svo_file = svo_file
		self.root = root + '/' \
			+ os.path.splitext(os.path.split(svo_file)[-1])[0] \
			+ '/'
		os.makedirs(self.root)

		print("{:15} {:>}".format("SVO Input: ", self.svo_file))
		print("{:15} {:>}".format("SVO Output: ", self.root))

	def format(self):
		init_params = sl.InitParameters()
		init_params.set_from_svo_file(self.svo_file)
		init_params.svo_real_time_mode = False
		init_params.coordinate_units = sl.UNIT.MILLIMETER

		zed = sl.Camera()

		error = zed.open(init_params)
		if not error is sl.ERROR_CODE.SUCCESS:
			sys.stdout.write(repr(error))
			zed.close()
			exit()
		
		# Camera information.
		information_formatter = InformationFormatter(self.root, zed)
		information_formatter.format()

		# Images.
		image_formatter = ImageFormatter(self.root, zed)
		image_formatter.format()

		zed.close()

class InformationFormatter(object):
	def __init__(self, root: str, camera: sl.Camera):
		self.root = root
		self.info = camera.get_camera_information()		
		self.extrinsics = self.info.calibration_parameters_raw
		self.left_intrinsics = \
			self.info.calibration_parameters_raw.left_cam
		self.right_intrinsics = \
			self.info.calibration_parameters_raw.right_cam

	def format(self):
		info_file_path = self.root + 'camera_information.txt'
		info_file = open(info_file_path, "w")
		info_file.write("Camera\n")
		info_file.write("{:15s} {:>10s}\n".format(
			"Model: ",
			self.info.camera_model))
		info_file.write("{:15s} {:10d}\n".format(
			"Serial no.: ",
			self.info.serial_number))
		info_file.write("{:15s} {:10d}\n".format(
			"Image width: ",
			self.info.camera_resolution.width))
		info_file.write("{:15s} {:10d}\n".format(
			"Image height: ",
			self.info.camera_resolution.height))
		info_file.write("{:15s} {:10.0f}\n".format(
			"FPS: ",
			self.info.camera_fps))

		info_file.write("\nExtrinsics\n")
		info_file.write("Rotation: \n{0}\n".format(
			self.extrinsics.R))
		info_file.write("Translation: \n{0}\n".format(
			self.extrinsics.T))
		
		info_file.write("\nIntrinsics - left\n")
		info_file.write("fx: {0}\n".format(self.left_intrinsics.fx))
		info_file.write("fy: {0}\n".format(self.left_intrinsics.fy))
		info_file.write("cx: {0}\n".format(self.left_intrinsics.cx))
		info_file.write("cy: {0}\n".format(self.left_intrinsics.cy))
		info_file.write("distortion: \n{0}\n".format(
			self.left_intrinsics.disto))

		info_file.write("\nIntrinsics - right\n")
		info_file.write("fx: {0}\n".format(self.right_intrinsics.fx))
		info_file.write("fy: {0}\n".format(self.right_intrinsics.fy))
		info_file.write("cx: {0}\n".format(self.right_intrinsics.cx))
		info_file.write("cy: {0}\n".format(self.right_intrinsics.cy))
		info_file.write("distortion: \n{0}\n".format(
			self.right_intrinsics.disto))
		
		info_file.close()

class ImageFormatter(object):
	def __init__(self, root: str, camera: sl.Camera, fill: int=8):
		assert root[-1] == '/', "Root directory must end with '/'."
		self.fill = fill
		self.camera = camera

		self.paths = dict()
		self.paths['root'] = root
		self.paths['left'] = root + 'left/'
		self.paths['right'] = root + 'right/'
			
		os.makedirs(self.paths['left'], exist_ok=True)
		os.makedirs(self.paths['right'], exist_ok=True)
	
	def format(self):
		# Image and timestamp conversion.
		left_image = sl.Mat()
		right_image = sl.Mat()
		timestamp = sl.Timestamp()

		runtime_params = sl.RuntimeParameters()
		runtime_params.sensing_mode = sl.SENSING_MODE.FILL
		n_frames = self.camera.get_svo_number_of_frames()

		sys.stdout.write('Converting SVO...\n')
		times_file = open(self.paths['root'] + 'times.txt',"w+")
		while True:
			if self.camera.grab(runtime_params) \
				!= sl.ERROR_CODE.SUCCESS:
				continue
		
			svo_position = self.camera.get_svo_position()
			self.camera.retrieve_image(left_image, 
				sl.VIEW.LEFT_UNRECTIFIED)
			self.camera.retrieve_image(right_image, 
				sl.VIEW.RIGHT_UNRECTIFIED)

			timestamp = self.camera.get_timestamp(
				sl.TIME_REFERENCE.IMAGE)
			milliseconds = timestamp.get_milliseconds()
		
			file_name = '{0}'.format(svo_position) \
				.zfill(self.fill) + '.png'
				
			left_image_file = self.paths['left'] + file_name
			right_image_file = self.paths['right'] + file_name

			# Write to files.
			cv2.imwrite(left_image_file, left_image.get_data())
			cv2.imwrite(right_image_file, right_image.get_data())

			times_file.write(str(milliseconds) + '\n')

			progress_bar((svo_position + 1) / n_frames * 100, 60)
			
			if svo_position >= (n_frames - 1):
				sys.stdout.write("\nSVO conversion ended.\n")
				break

