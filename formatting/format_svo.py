import argparse
import cv2
import pyzed.sl as sl
import sys

from format import Format, format_from_string, SVOFormatter

def format_svo(svo_file: str, format: Format):
	if format == Format.Default:
		formatter = SVOFormatter(svo_file)
		formatter.format()

def main():
	parser = argparse.ArgumentParser(description='Formats a SVO file to \
		to the specified format.')
	parser.add_argument('-i', type=str, help='input file', 
		required=True)
	parser.add_argument('-f', type=str, help='output format',
		default="Default", choices=["Default"])
	args = parser.parse_args()

	format_svo(args.i, format_from_string(args.f))

if __name__ == '__main__':
	main()
