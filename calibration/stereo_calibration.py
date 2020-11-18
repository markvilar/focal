import argparse

from typing import List

from intrinsic import IntrinsicCalibrator
from extrinsic import ExtrinsicCalibrator

def stereo_calibration(root: str, indices: List[int]):
	left_calibrator = IntrinsicCalibrator(root + 'left_unrectified/', 
		[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])
	right_calibrator = IntrinsicCalibrator(root + 'right_unrectified/',
		[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])

	left_calibrator.load_images()
	#left_calibrator.calibrate()

def main():
	parser = argparse.ArgumentParser(description='Performs intrinsic and \
		extrinsic calibration for a stereo camera.')
	parser.add_argument('-i', type=str, help='input directory',
		required=True)
	parser.add_argument('-f', type=List[int], help='image indices')
	args = parser.parse_args()

	stereo_calibration(args.i, args.f)

if __name__ == '__main__':
	main()
