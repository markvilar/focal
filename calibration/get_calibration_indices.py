import argparse

from inspector import StereoInspector

def get_calibration_indices(directory: str):
	inspector = StereoInspector(directory)
	inspector.inspect()

def main():
	parser = argparse.ArgumentParser(description="Inspect a sequence of " \
		"PNG image files and store the selected indices.")
	parser.add_argument("-i", type=str, help="input directory")
	args = parser.parse_args()
	get_calibration_indices(args.i)

if __name__ == '__main__':
	main()
