clear;
clc;

inputDirectory = '/home/martin/dev/reproject/right';
outputDirectory = '/home/martin/dev/reproject/right-calibration';
separator = '/';
extension = 'png';

nRadialCoefs = 2;
squareSize = 25;  % in units of 'millimeters'

% Sanity check.
assert(isa(outputDirectory, 'char'), "Output directory must be a char.");
assert(nRadialCoefs <= 3, "Cannot calculate more than 3 radial coeffcients.");

% Get image file names.
imageFiles = GetImageFileNames(inputDirectory, separator, extension);

% Detect checkboard pattern.
[imagePoints, boardSize, imagesUsed] = detectCheckerboardPoints(imageFiles);
imageFiles = imageFiles(imagesUsed);

% Read the first image to obtain image size
originalImage = imread(imageFiles{1});
[mrows, ncols, ~] = size(originalImage);

% Generate world coordinates of the corners of the squares
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% Calibrate the camera
[cameraParams, imagesUsed, estimationErrors] = estimateCameraParameters(...
    imagePoints, worldPoints, ...
    'EstimateSkew', false, ...
    'EstimateTangentialDistortion', true, ...
    'NumRadialDistortionCoefficients', nRadialCoefs, 'WorldUnits', ...
    'millimeters', 'InitialIntrinsicMatrix', [], ...
    'InitialRadialDistortion', [], 'ImageSize', [mrows, ncols]); 

% Display errors.
displayErrors(estimationErrors, cameraParams);

SaveCalibrationData(outputDirectory, imageFiles, cameraParams, ...
    estimationErrors, separator);