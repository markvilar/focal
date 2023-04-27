import argparse

from pathlib import Path
from typing import List

import pandas as pd
import tqdm

from nav.naviwrap import read_survey_log
from nav.sensors import ApsParser, CompassParser

def export(paths: List[Path]) -> None:
    """ """
    for path in paths:
        # NOTE: Set up proper reading of log header
        header, samples = naviwrap.read_survey_log(path, skip=51)
        print(header)
        print("Samples: {0}".format(len(samples)))

        # NOTE: Revise sensor collectors for position and heading. Can also
        # include position, heading, depth and altitude from the old setup.
        position_formatter = ApsParser(zone=32, letter="N")
        gyro_formatter = CompassParser()

        # TODO: Collect samples
        for sample in tqdm.tqdm(samples, desc="Processing navigation log..."):
            position_formatter.parse(sample)
            gyro_formatter.parse(sample)

        input()

        # TODO: Filter
        # TODO: Merge sensors
    
    # TODO: Merge logs to navigation table

def process_arguments(args):
    paths = list()
    for log in args.logs:
        paths.append(Path(log))
    return paths


def main():
    parser = argparse.ArgumentParser(
        description="Merge Navipac logs and export data as CSV files.")
    parser.add_argument("--logs", nargs="+", help="navigation logs")

    paths = process_arguments(parser.parse_args())
    
    export(paths)

if __name__ == "__main__":
    main()
