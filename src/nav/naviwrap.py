from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import tqdm

#NOTE: From 2016 survey log:
"""
H0; P; O; no; Time; E; N; height; stddev; ; ; ; kp; dal; dol; fix /H0
H0; P; D; no; Time; E; N; height; stddev; dx; dy; dz; kp; dal; dol /H0
H0; D; no; insttype; index; channel_number; Time; BathyDepth; NumOfDepths; 
    Depth1; TimeAge1../H0
H0; A; no; index; Time; Roll; Pitch; Heave /H0
H0; G; no; index;  type; Time; Gyro; CMG /H0
"""

@dataclass
class SurveyLogHeader():
    # TODO: Implement
    pass


@dataclass
class SurveyLogSample():
    type: str
    source: int
    time: str
    data: List[str] = field(default_factory=list())


def format_sample(line: List[str]) -> SurveyLogSample:
    """ Formats a list of strings to Navipac survey samples. """
    stripped = [word.strip() for word in line.split(";")]
    if len(stripped) < 4:
        return None
    
    type = stripped[0]
    if type == "P":
        sample = SurveyLogSample(type=type, source=int(stripped[2]), 
            time=stripped[3], data=stripped[4:])
    elif type == "S":
        sample = SurveyLogSample(type=type, source=int(stripped[1]), 
            time=stripped[2], data=stripped[3:])
    elif type == "G":
        sample = SurveyLogSample(type=type, source=int(stripped[1]), 
            time=stripped[3], data=stripped[4:])
    elif type == "V":
        sample = SurveyLogSample(type=type, source=int(stripped[2]), 
            time=stripped[3], data=stripped[4:])
    else:
        return None
    return sample


def read_survey_log(path: Path, skip: int=0) \
    -> Tuple[SurveyLogHeader, List[SurveyLogSample]]:
    """ Reads a Navipac survey log and returns the header information and
    data samples."""
    # Open and read file
    lines = []
    with open(path, "r", encoding="utf8", errors="ignore") as handle:
        lines = handle.readlines()

    assert skip < len(lines), "skip is out of bounds of lines"
    header_lines = lines[:skip]
    sample_lines = lines[skip:]
    
    # TODO: Process header

    # Process samples
    samples = []
    for index, line in tqdm.tqdm(enumerate(sample_lines), 
        desc="Reading log samples..."):
        sample = format_sample(line)
        if sample: samples.append(sample)
    return (SurveyLogHeader(), samples)
