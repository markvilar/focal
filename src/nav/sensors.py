from dataclasses import dataclass, field
from typing import List

import arrow
import pandas as pd
import utm

from .naviwrap import SurveyLogSample


@dataclass
class ApsParser():
    zone: int
    letter: str
    time_format: str="YYYY:MM:DD:HH:mm:ss.SSS"
    data: pd.DataFrame = pd.DataFrame(columns=["datetime", "latitude", 
        "longitude", "down"])

    def parse(self, sample: SurveyLogSample) -> None:
        datetime = arrow.get(sample[3], self.time_format)
        easting = float(sample[4])
        northing = float(sample[5])
        down = float(sample[6])
        latitude, longitude = utm.to_latlon(easting, northing, self.zone, 
            self.letter)
        self.data.loc[len(self.data)] = { "datetime"  : datetime,
            "latitude" : latitude, "longitude" : longitude, "down" : down }


@dataclass
class CompassValidator():
    tag: str="G"
    code: str="52"
    id: str="2"

    def is_valid(self, sample: List[str]) -> bool:
        valid_length = len(sample) == 6
        valid_header = sample[0] == self.tag \
            and sample[1] == self.code \
            and sample[2] == self.id
        return valid_length and valid_header


@dataclass
class CompassParser():
    time_format: str="YYYY:MM:DD:HH:mm:ss.SSS"
    data: pd.DataFrame = pd.DataFrame(columns=["datetime", "heading"])

    def parse(self, sample: List[str]) -> None:
        """ """
        if not self.is_valid(sample): 
            return
        datetime = arrow.get(sample[3], self.time_format)
        heading = float(sample[4])
        self.data.loc[len(self.data)] = { "datetime" : datetime, 
            "heading"  : heading }

    def get_data(self) -> pd.DataFrame:
        return self.data
