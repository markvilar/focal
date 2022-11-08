import argparse

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import tqdm

from image import types, io
from zed.dataloaders import FrameLoader

@dataclass
class ExportArguments:
    input: Path
    output: Path
    start: int
    stop: int
    step: int
    stereo: bool
    format: Optional[types.ImageFileFormat]=None


def process_arguments(args) -> ExportArguments:
    """ """
    input = Path(args.input)
    output = Path(args.output)
    start = args.start
    stop = args.stop
    step = args.step
    stereo = args.stereo

    assert start >= 0, "start index cannot be negative"
    assert stop > start, "stop index cannot be lower than start index"
    assert step > 0, "step must be a positive integer"

    return ExportArguments(input=input, output=output, start=start, 
        stop=stop, step=step, stereo=stereo)


def export(arguments: ExportArguments) -> None:
    """ """
    loader = FrameLoader(filepath=arguments.input, 
        index=arguments.start,
        stop=arguments.stop,
        step=arguments.step)

    loader.prepare()

    n = int((arguments.stop - arguments.start) / arguments.step)

    with tqdm.tqdm(total=n) as bar:
        while loader.has_frame():
            index, time, left, right = loader.load_frame()

            filename = time.format('YYYYMMDD_HHmmss_SSS') + ".jpg"
            left_dir = arguments.output / "left"
            right_dir = arguments.output / "right"

            io.save_image(left, left_dir / filename)
            io.save_image(right, right_dir / filename)

            bar.update(1)

def main():
    parser = argparse.ArgumentParser(
        description="Export the images from a SVO file to common image files.")
    parser.add_argument("--input", type=str, help="input svo file")
    parser.add_argument("--output", type=str, help="output directory")
    parser.add_argument("--start", type=int, help="start frame index")
    parser.add_argument("--stop", type=int, help="stop frame index")
    parser.add_argument("--step", type=int, default=1, help="frame step")
    parser.add_argument('--stereo', default=False, action='store_true')
    parser.add_argument('--no-stereo', dest='stereo', action='store_false')

    # /home/martin/data/20221031_skarnsundet/stereo/20221102_142759.svo

    arguments = process_arguments(parser.parse_args())

    export(arguments)

if __name__ == "__main__":
    main()
