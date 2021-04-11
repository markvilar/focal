% -------------------------------------------------------------------------
% ---- Setup --------------------------------------------------------------
% -------------------------------------------------------------------------

clear;
clc;

% Suppress warnings.
warning('off','all')

% -------------------------------------------------------------------------
% ---- Variables ----------------------------------------------------------
% -------------------------------------------------------------------------

% Input.
inputDir = strcat('/home/martin/data/calibration-experiment/', ...
    'sequence-02/subset-04/');
outputDir = strcat('/home/martin/data/calibration-experiment/', ...
    'sequence-02/subset-04/results-radial/');

% Calibration variables.
squareSize = 40; % Square size in millimeters.
numRadialCoefficients = 3;
optionTangential = false;
optionSkew = false;

% Display variables.
optionDisplayExtrinsics = false;
optionDisplayImages = false;

% -------------------------------------------------------------------------
% ---- Image dataloaders --------------------------------------------------
% -------------------------------------------------------------------------

% Set up image dataloaders.
leftImages = imageDatastore(fullfile(inputDir, 'left', '*.png'));
rightImages = imageDatastore(fullfile(inputDir, 'right', '*.png'));

% Get image sizes.
leftImageSize = [size(readimage(leftImages, 1), 1), ...
    size(readimage(leftImages, 1), 2)];
rightImageSize = [size(readimage(rightImages, 1), 1), ...
    size(readimage(rightImages, 1), 2)];

% -------------------------------------------------------------------------
% ---- Detect checkerboard ------------------------------------------------
% -------------------------------------------------------------------------

% Detect the checkerboards.
fprintf('\nDetecting checkerboard points...');
[imagePoints, boardSize, usedImages] = detectCheckerboardPoints(...
     leftImages.Files, rightImages.Files);

% Specify world coordinates of checkerboard keypoints.
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% -------------------------------------------------------------------------
% ---- Calibrate camera ---------------------------------------------------
% -------------------------------------------------------------------------

fprintf('\nCalibrating stereo camera...');
[stereoCamera, usedImagePairs, stereoErrors] = estimateCameraParameters(...
        imagePoints, worldPoints, ...
        'EstimateSkew', optionSkew, ...
        'EstimateTangentialDistortion', optionTangential, ...
        'NumRadialDistortionCoefficients', numRadialCoefficients, ...
        'WorldUnits', 'millimeters', ...
        'InitialIntrinsicMatrix', [], ...
        'InitialRadialDistortion', [], ...
        'ImageSize', leftImageSize);


% -------------------------------------------------------------------------
% ---- Visualize calibration results --------------------------------------
% -------------------------------------------------------------------------

if (optionDisplayExtrinsics)
    figure;
    showReprojectionErrors(stereoCamera);
    figure;
    showExtrinsics(stereoCamera);
    shg;
end

% -------------------------------------------------------------------------
% ---- Save calibration results -------------------------------------------
% -------------------------------------------------------------------------

fprintf('\nSaving calibration results...\n');
SaveStereoCameraCalibration(outputDir, leftImages, rightImages, ...
    stereoCamera, '/', optionDisplayImages);