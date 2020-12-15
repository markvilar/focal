import argparse

from typing import List, Tuple

from intrinsic import IntrinsicCalibrator
from extrinsic import ExtrinsicCalibrator

def calibrate_stereo(left_directory: str, right_directory: str, 
	pattern_size: Tuple[int, int], tile_size: float):
	left_calibrator = IntrinsicCalibrator(left_directory, pattern_size,
		tile_size)
	right_calibrator = IntrinsicCalibrator(right_directory, pattern_size,
		tile_size)

	left_calibrator.calibrate()
	#right_calibrator.calibrate()

def main():
	parser = argparse.ArgumentParser(description='Performs intrinsic and \
		extrinsic calibration for a stereo camera.')
	parser.add_argument('-left', type=str, 
		help='Left image input directory', required=True)
	parser.add_argument('-right', type=str, 
		help='Right image input directory', required=True)
	parser.add_argument('-layout', type=int, 
		help='Checkerboard pattern layout', nargs='+')
	parser.add_argument('-size', type=float, 
		help='Checkerboard tile size.')
	args = parser.parse_args()

	calibrate_stereo(args.left, args.right, tuple(args.layout), args.size)

if __name__ == '__main__':
	main()
