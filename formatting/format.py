import enum
import os
import sys

import cv2
import pyzed.sl as sl

from utilities import progress_bar

class Format(enum.Enum):
	ORBSlam = 1

def format_from_string(string: str) -> Format:
	if string == "ORBSlam":
		return Format.ORBSlam
	else:
		return None

class ORBSlamFormatter:
	def __init__(self, svo_file, output_root):
		self.input = svo_file
		self.output = dict()
		self.output['root'] = output_root

	def validate_input(self):
		if not os.path.exists(self.input):
			raise Exception('Input file does not exists.')
		if os.path.splitext(self.input)[-1].lower() != ".svo":
			raise Exception('Input file is not a SVO file.')

	def validate_output(self):
		if not os.path.exists(self.output['root']):
			raise Exception('Output folder does not exist.')

		self.output['left'] = self.output['root'] + '/left'
		self.output['right'] = self.output['root'] + '/right'
		
		os.makedirs(self.output['left'], exist_ok=True)
		os.makedirs(self.output['right'], exist_ok=True)

	def format(self):
		self.validate_input()
		self.validate_output()
		
		init_params = sl.InitParameters()
		init_params.set_from_svo_file(self.input)
		init_params.svo_real_time_mode = False
		init_params.coordinate_units = sl.UNIT.MILLIMETER

		zed = sl.Camera()

		error = zed.open(init_params)
		if not error is sl.ERROR_CODE.SUCCESS:
			sys.stdout.write(repr(error))
			zed.close()
			exit()

		left_image = sl.Mat()
		right_image = sl.Mat()
		timestamp = sl.Timestamp()

		runtime_params = sl.RuntimeParameters()
		runtime_params.sensing_mode = sl.SENSING_MODE.FILL
		n_frames = zed.get_svo_number_of_frames()

		sys.stdout.write('Converting SVO...\n')
		while True:
			if zed.grab(runtime_params) != sl.ERROR_CODE.SUCCESS:
				continue
		
			svo_position = zed.get_svo_position()
			zed.retrieve_image(left_image, sl.VIEW.LEFT)
			zed.retrieve_image(right_image, sl.VIEW.RIGHT)
			timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
			milliseconds = timestamp.get_milliseconds()
			
			left_filename = self.output['left'] + '/' \
				+ 'left_{0}.png'.format(milliseconds)
			right_filename = self.output['right'] + '/' \
				+ 'right_{0}.png'.format(milliseconds)

				
			cv2.imwrite(left_filename, left_image.get_data())
			cv2.imwrite(right_filename, right_image.get_data())

			progress_bar((svo_position + 1) / n_frames * 100, 60)
			
			if svo_position >= (n_frames - 1):
				sys.stdout.write("\nSVO conversion ended.\n")
				break

		zed.close()
