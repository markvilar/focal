clear;
clc;

% -------------------------------------------------------------------------
% ---- Variables ----------------------------------------------------------
% -------------------------------------------------------------------------

% Input.
inputDir = strcat('/home/martin/data/calibration-experiment/', ...
    'sequence-02/subset-04/');
outputDir = strcat('/home/martin/data/calibration-experiment/', ...
    'sequence-02/subset-04/results/');

% Calibration variables.
squareSize = 40; % Square size in millimeters.
numRadialCoefficients = 2;
optionTangential = false;
optionSkew = false;

% Display variables.
optionDisplay = false;

% -------------------------------------------------------------------------
% ---- Image dataloaders --------------------------------------------------
% -------------------------------------------------------------------------

% Set up image dataloaders.
images = imageDatastore(fullfile(inputDir, {'left', 'right'}));
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

if (optionDisplay)
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
    stereoCamera, '/', optionDisplay);

% TODO: Rectify the stereo images.
%[J1, J2] = rectifyStereoImages(I1, I2, stereoParams);
