clear;
clc;

% Calibration variables.
squareSize = 40;
units = "millimeters";

% Calibration parameters.
numberOfRadialCoefficients = 2;
tangentialDistortion = false;
skew = false;

% Options.
optionDisplayExtrinsics = false;
optionDisplayImages = false;
optionSaveImages = false;

inputDirectory = strcat("/home/martin/data/Calibration-Experiments/", ...
    "Calibration-Images-02/");
outputDirectory = strcat("/home/martin/dev/Focal/Output/", ...
    "Calibration-Results/Calibration-02/");

CalibrateStereoCamera(inputDirectory, outputDirectory, ...
    squareSize, units, numberOfRadialCoefficients, ...
    tangentialDistortion, skew, ...
    optionDisplayExtrinsics, optionDisplayImages, optionSaveImages);