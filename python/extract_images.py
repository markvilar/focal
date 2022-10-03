import argparse

from svo import SVOInspector

def extract_images(svo_file: str, output_dir: str, start_index: int, 
    bias: float):
	inspector = SVOInspector(svo_file, output_dir, start_index, bias)
	inspector.inspect()

def main():
    parser = argparse.ArgumentParser(description="Inspect the video \
        stream from a SVO file and store the marked images.")
    parser.add_argument("-i", type=str, help="Input SVO file.")
    parser.add_argument("-o", type=str, help="Output folder.")
    parser.add_argument("-s", type=int, help="SVO start index.")
    parser.add_argument("-bias", type=float, default=0.0, help="Time bias.")
    args = parser.parse_args()

    extract_images(args.i, args.o, args.s, args.bias)

if __name__ == '__main__':
	main()
