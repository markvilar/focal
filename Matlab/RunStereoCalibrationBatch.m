clear;
clc;

% Calibration variables.
squareSize = 40;
units = "millimeters";

% Options.
optionDisplayExtrinsics = false;
optionDisplayImages = false;
optionSaveImages = false;

inputDirectory = strcat("/home/martin/data/calibration-experiment/", ...
    "sequence-02/subset-04/");
outputDirectory = strcat("/home/martin/dev/Focal/Output/", ...
    "Calibration-Results/");

CalibrateStereoCamera(inputDirectory, ...
    strcat(outputDirectory, "Calibration-01/"), ...
    squareSize, units, 2, false, false, ...
    optionDisplayExtrinsics, optionDisplayImages, optionSaveImages);