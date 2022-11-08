from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Protocol, Tuple

import arrow
import pandas as pd
import tqdm
import utm

class SampleFormatter(Protocol):
    def is_valid(self, sample: List[str]) -> bool:
        ...

    def insert(self, sample: List[str]) -> None:
        ...

    def get_data(self) -> pd.DataFrame:
        ...


@dataclass
class SurveyLogReader():

    def read(self, path: Path, skip: int=0) -> List[List[str]]:
        """ """
        # Open and read file
        lines = []
        with open(path, "r", encoding="utf8", errors="ignore") as handle:
            lines = handle.readlines()

        assert skip < len(lines), "skip is out of bounds of lines"
        lines = lines[skip:]
        for index, line in enumerate(lines):
            lines[index] = [word.strip() for word in line.split(";")]
        return lines


@dataclass
class HipapFormatter():
    zone: int
    letter: str
    time_format: str="YYYY:MM:DD:HH:mm:ss.SSS"
    data: pd.DataFrame = pd.DataFrame(columns=["datetime", "latitude", 
        "longitude", "down", "easting", "northing", "zone", "letter"])

    def is_valid(self, sample: List[str]) -> bool:
        return len(sample) == 16 and sample[0] == "P" and sample[1] == "X" \
            and sample[2] == "802"

    def insert(self, sample: List[str]) -> None:
        """ """
        if not self.is_valid(sample):
            return
        datetime = arrow.get(sample[3], self.time_format)
        easting = float(sample[4])
        northing = float(sample[5])
        down = float(sample[6])
        latitude, longitude = utm.to_latlon(easting, northing, self.zone, 
            self.letter)
        self.data.loc[len(self.data)] = {
                "datetime"  : datetime,
                "latitude"  : latitude,
                "longitude" : longitude,
                "down"      : down,
                "easting"   : easting,
                "northing"  : northing,
                "zone"      : self.zone,
                "letter"    : self.letter,
            }

    def get_data(self) -> pd.DataFrame:
        return self.data


@dataclass
class CompassFormatter():
    time_format: str="YYYY:MM:DD:HH:mm:ss.SSS"
    data: pd.DataFrame = pd.DataFrame(columns=["datetime", "heading"])

    def is_valid(self, sample: List[str]) -> bool:
        return len(sample) == 6 and sample[0] == "G" and sample[1] == "52" \
            and sample[2] == "2"

    def insert(self, sample: List[str]) -> None:
        """ """
        if not self.is_valid(sample): 
            return
        datetime = arrow.get(sample[3], self.time_format)
        heading = float(sample[4])
        self.data.loc[len(self.data)] = {
                "datetime" : datetime, 
                "heading"  : heading
            }

    def get_data(self) -> pd.DataFrame:
        return self.data
