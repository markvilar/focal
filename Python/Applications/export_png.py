import argparse

from export import export_png

def main():
    parser = argparse.ArgumentParser(description="Export the images from a \
        SVO file as PNG files.")
    parser.add_argument("--input", type=str, \
        help="Input SVO file.")
    parser.add_argument("--output", type=str, \
        help="Output directory.")
    parser.add_argument("--start", type=int, \
        help="Start index.")
    parser.add_argument("--stop", type=int, \
        help="Stop index.")
    parser.add_argument("--skip", type=int, \
        help="Index skip.")
    parser.add_argument("--offset", type=int, default=0, \
        help="Frame index offset.")
    parser.add_argument("--stereo", type=bool, default=False, \
        help="Extract stereo images.")
    parser.add_argument("--grayscale", type=bool, default=True, \
        help="Extract grayscale images.")
    parser.add_argument("--rectify", type=bool, default=True, \
        help="Rectify images.")
    parser.add_argument("--preprocess", type=bool, default=True, \
        help="Preprocess images.")
    args = parser.parse_args()

    export_png(args.input, args.output, args.start, args.stop, args.skip, \
        args.offset, args.stereo, args.grayscale, args.rectify, \
        args.preprocess)

if __name__ == "__main__":
    main()
