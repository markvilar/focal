import argparse
import cv2
import pyzed.sl as sl
import sys

from format import Format, format_from_string, ORBSlamFormatter

def format_svo(svo_file: str, output_dir: str, format: Format):
	if format == Format.ORBSlam:
		formatter = ORBSlamFormatter(svo_file, output_dir)
		formatter.format()

def main():
	parser = argparse.ArgumentParser(description='Formats a SVO file to \
		to the specified format.')
	parser.add_argument('-i', type=str, help='input file', 
		required=True)
	parser.add_argument('-o', type=str, help='output root directory', 
		required=True)
	parser.add_argument('-f', type=str, help='output format',
		default="ORBSlam", choices=["ORBSlam"])
	args = parser.parse_args()

	format_svo(args.i, args.o, format_from_string(args.f))

if __name__ == '__main__':
	main()
