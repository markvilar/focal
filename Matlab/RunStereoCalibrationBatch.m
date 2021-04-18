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

% -------------------------------------------------------------------------
% ---- Model 1 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(inputDirectory, ...
    strcat(outputDirectory, "Calibration-01/"), ...
    squareSize, units, 2, false, false, ...
    optionDisplayExtrinsics, optionDisplayImages, optionSaveImages);

% -------------------------------------------------------------------------
% ---- Model 2 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(inputDirectory, ...
    strcat(outputDirectory, "Calibration-02/"), ...
    squareSize, units, 3, false, false, ...
    optionDisplayExtrinsics, optionDisplayImages, optionSaveImages);

% -------------------------------------------------------------------------
% ---- Model 3 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(inputDirectory, ...
    strcat(outputDirectory, "Calibration-03/"), ...
    squareSize, units, 2, true, false, ...
    optionDisplayExtrinsics, optionDisplayImages, optionSaveImages);

% -------------------------------------------------------------------------
% ---- Model 4 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(inputDirectory, ...
    strcat(outputDirectory, "Calibration-04/"), ...
    squareSize, units, 3, true, false, ...
    optionDisplayExtrinsics, optionDisplayImages, optionSaveImages);