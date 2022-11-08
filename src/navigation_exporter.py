import argparse

from pathlib import Path
from typing import List

import pandas as pd
import tqdm

from nav import naviwrap


def export(paths: List[Path]) -> None:
    """ """
    for path in paths:
        reader = naviwrap.SurveyLogReader()
        samples = reader.read(path, skip=51)

        hipap_formatter = naviwrap.HipapFormatter(zone=32, letter="N")
        compass_formatter = naviwrap.CompassFormatter()

        for sample in tqdm.tqdm(samples, desc="Processing navigation log..."):
            hipap_formatter.insert(sample)
            compass_formatter.insert(sample)

        print(hipap_formatter.get_data())
        print(compass_formatter.get_data())
        input()

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
