import argparse

from zed.svo import SVOInspector

def extract_images(svo_file: str, output_dir: str, start_index: int, \
    bias: float, save_right: bool):
	inspector = SVOInspector(svo_file, output_dir, start_index, bias, \
        save_right)
	inspector.inspect()

def main():
    parser = argparse.ArgumentParser(description="Inspect the video \
        stream from a SVO file and store the marked images.")
    parser.add_argument("-i", type=str, help="Input SVO file.")
    parser.add_argument("-o", type=str, help="Output folder.")
    parser.add_argument("-s", type=int, help="SVO start index.")
    parser.add_argument("-bias", type=float, help="Time bias.")
    parser.add_argument("--save-right", dest="save_right", default=False, 
        action="store_true")
    parser.add_argument("--no-save-right", dest="save_right", 
        action="store_false", help="Save right side images.")
    args = parser.parse_args()
    extract_images(args.i, args.o, args.s, args.bias, args.save_right)

if __name__ == '__main__':
	main()
