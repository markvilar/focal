import argparse
import cv2
import pyzed.sl as sl
import sys

from svo import Format, format_from_string, SVOFormatter

def format_svo(svo_file: str):
	formatter = SVOFormatter(svo_file)
	formatter.format()

def main():
	parser = argparse.ArgumentParser(description='Formats a SVO file to \
		to the specified format.')
	parser.add_argument('-i', type=str, help='input file', 
		required=True)
	args = parser.parse_args()

	format_svo(args.i)

if __name__ == '__main__':
	main()
