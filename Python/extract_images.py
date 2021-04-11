import argparse

from svo import SVOInspector

def extract_images(svo_file: str, output_dir: str, start_index: int):
	inspector = SVOInspector(svo_file, output_dir, start_index)
	inspector.inspect()

def main():
	parser = argparse.ArgumentParser(description="Inspect the video \
		stream from a SVO file and store the marked images.")
	parser.add_argument("-i", type=str, help="input svo")
	parser.add_argument("-o", type=str, help="output folder")
	parser.add_argument("-s", type=int, help="start index")
	args = parser.parse_args()
	extract_images(args.i, args.o, args.s)

if __name__ == '__main__':
	main()
