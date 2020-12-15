clear;
clc;

% Variables.
rootDir = '/home/martin/dev/focal/data/';
squareSize = 25;

nRadialCoefs = 2;
estimateTangential = true;
estimateSkew = false;

rotationThreshold = 10 * pi / 180;
translationThreshold = 15;

% Set up dataloaders.
imageDir = fullfile(rootDir, 'calibration');
leftImages = imageDatastore(fullfile(imageDir,'left'));
rightImages = imageDatastore(fullfile(imageDir,'right'));

%Detect the checkerboards.
[imagePoints, boardSize] = detectCheckerboardPoints(...
     leftImages.Files, rightImages.Files);

%Specify world coordinates of checkerboard keypoints. The square size is in millimeters.
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

%Calibrate the stereo camera system. Here both cameras have the same resolution.
I = readimage(leftImages,1); 
imageSize = [size(I, 1), size(I, 2)];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Calibrate intrinsics of left camera. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[leftCamera, leftImages, leftErrors] = estimateCameraParameters(...
    squeeze(imagePoints(:, :, :, 1)), worldPoints, ...
    'EstimateSkew', estimateSkew, ...
    'EstimateTangentialDistortion', estimateTangential, ...
    'NumRadialDistortionCoefficients', nRadialCoefs, ...
    'WorldUnits', 'millimeters', ...
    'InitialIntrinsicMatrix', [], ...
    'InitialRadialDistortion', [], ...
    'ImageSize', imageSize); 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Calibrate intrinsics of the right camera. %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[rightCamera, rightImages, rightErrors] = estimateCameraParameters(...
    squeeze(imagePoints(:, :, :, 2)), worldPoints, ...
    'EstimateSkew', estimateSkew, ...
    'EstimateTangentialDistortion', estimateTangential, ...
    'NumRadialDistortionCoefficients', nRadialCoefs, ...
    'WorldUnits', 'millimeters', ...
    'InitialIntrinsicMatrix', [], ...
    'InitialRadialDistortion', [], ...
    'ImageSize', imageSize);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Calibrate extrinsics of the stereo camera. %%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[stereoCamera, ~, stereoErrors] = estimateStereoBaseline(...
    imagePoints, worldPoints, leftCamera, rightCamera);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Filter out outliers. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

rotationErrors = stereoErrors.Camera1ExtrinsicsErrors.RotationVectorsError;
translationErrors = stereoErrors.Camera1ExtrinsicsErrors.TranslationVectorsError;

rotationFilter = any(rotationErrors > rotationThreshold, 2);
translationFilter = any(translationErrors > translationThreshold, 2);
filter = not(or(rotationFilter, translationFilter));

filteredImagePoints = imagePoints(:, :, filter, :);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Calibrate extrinsics of the stereo camera. %%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[filteredStereoCamera, imagePairs, filteredStereoErrors] = ...
    estimateStereoBaseline(filteredImagePoints, worldPoints, ...
    leftCamera, rightCamera);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Visualize calibration results. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

displayErrors(leftErrors, leftCamera);

displayErrors(rightErrors, rightCamera);

figure;
showReprojectionErrors(stereoCamera);

figure;
showReprojectionErrors(filteredStereoCamera);

figure;
showExtrinsics(stereoCamera);

figure;
showExtrinsics(filteredStereoCamera);