clear;
clc;

% Calibration variables.
squareSize = 0.040; % Square size in meters.
numberRadialCoefficients = 3;
optionTangential = false;
optionSkew = false;

% Display variables.
optionDisplayExtrinsics = false;
optionDisplayImages = false;

rootDirectory = strcat("/home/martin/data/calibration-experiment/", ...
    "sequence-02/");

% -------------------------------------------------------------------------
% ---- Model 1 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(strcat(rootDirectory, "subset-04/"), ...
    strcat(rootDirectory, "Calibration-01/"), ...
    squareSize, 2, false, false, ...
    optionDisplayExtrinsics, optionDisplayImages);

% -------------------------------------------------------------------------
% ---- Model 2 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(strcat(rootDirectory, "subset-04/"), ...
    strcat(rootDirectory, "Calibration-02/"), ...
    squareSize, 3, false, false, ...
    optionDisplayExtrinsics, optionDisplayImages);

% -------------------------------------------------------------------------
% ---- Model 3 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(strcat(rootDirectory, "subset-04/"), ...
    strcat(rootDirectory, "Calibration-03/"), ...
    squareSize, 2, true, false, ...
    optionDisplayExtrinsics, optionDisplayImages);

% -------------------------------------------------------------------------
% ---- Model 4 ------------------------------------------------------------
% -------------------------------------------------------------------------

CalibrateStereoCamera(strcat(rootDirectory, "subset-04/"), ...
    strcat(rootDirectory, "Calibration-04/"), ...
    squareSize, 3, true, false, ...
    optionDisplayExtrinsics, optionDisplayImages);