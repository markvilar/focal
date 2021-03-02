clear;
clc;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Variables. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Input.
rootDir = '/home/martin/data/tbs-calibration/tbs-calibration-02/';
subsetDir = 'subset-04/';
inputDir = strcat(rootDir, subsetDir);

% Output
outputDir = strcat(rootDir, 'subset04-results/');
parameterFile = 'parameter.txt';
errorFile = 'calibration-errors.csv';
parameterPath = strcat(rootDir, parameterFile);

% Calibration variables.
optionSimultaneousCalibration = true;
squareSize = 40; % Square size in millimeters.
numRadialCoefficients = 2;
optionTangential = false;
optionSkew = false;

% Display variables.
optionDisplay = true;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Image dataloaders. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set up image dataloaders.
images = imageDatastore(fullfile(inputDir, {'left', 'right'}));
leftImages = imageDatastore(fullfile(inputDir, 'left', '*.png'));
rightImages = imageDatastore(fullfile(inputDir, 'right', '*.png'));

% Get image sizes.
leftImageSize = [size(readimage(leftImages, 1), 1), ...
    size(readimage(leftImages, 1), 2)];
rightImageSize = [size(readimage(rightImages, 1), 1), ...
    size(readimage(rightImages, 1), 2)];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Detect checkerboard. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Detect the checkerboards.
fprintf('\nDetecting checkerboard points...');
[imagePoints, boardSize, usedImages] = detectCheckerboardPoints(...
     leftImages.Files, rightImages.Files);

% Specify world coordinates of checkerboard keypoints.
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Calibrate camera. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (optionSimultaneousCalibration)
    fprintf('\nCalibrating stereo camera...');
    [stereoCamera, usedImagePairs, stereoErrors] = ...
        estimateCameraParameters(imagePoints, worldPoints, ...
            'EstimateSkew', optionSkew, ...
            'EstimateTangentialDistortion', optionTangential, ...
            'NumRadialDistortionCoefficients', numRadialCoefficients, ...
            'WorldUnits', 'millimeters', ...
            'InitialIntrinsicMatrix', [], ...
            'InitialRadialDistortion', [], ...
            'ImageSize', leftImageSize);
else
    fprintf('\nCalibrating left camera intrinsics...');
    [leftCamera, leftDetection, leftErrors] = estimateCameraParameters(...
        squeeze(imagePoints(:, :, :, 1)), worldPoints, ...
        'EstimateSkew', optionSkew, ...
        'EstimateTangentialDistortion', optionTangential, ...
        'NumRadialDistortionCoefficients', numRadialCoefficients, ...
        'WorldUnits', 'millimeters', ...
        'InitialIntrinsicMatrix', [], ...
        'InitialRadialDistortion', [], ...
        'ImageSize', leftImageSize); 

    fprintf('\nCalibrating right camera intrinsics...');
    [rightCamera, rightDetection, rightErrors] = ....
        estimateCameraParameters(squeeze(imagePoints(:, :, :, 2)), ...
        worldPoints, ...
        'EstimateSkew', optionSkew, ...
        'EstimateTangentialDistortion', optionTangential, ...
        'NumRadialDistortionCoefficients', numRadialCoefficients, ...
        'WorldUnits', 'millimeters', ...
        'InitialIntrinsicMatrix', [], ...
        'InitialRadialDistortion', [], ...
        'ImageSize', rightImageSize);

    fprintf('\nCalibrating stereo camera extrinsics...');
    [stereoCamera, usedImagePairs, stereoErrors] = ...
        estimateStereoBaseline(imagePoints, worldPoints, leftCamera, ...
            rightCamera);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Visualize calibration results. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if (optionDisplay)
    figure;
    showReprojectionErrors(stereoCamera);
    figure;
    showExtrinsics(stereoCamera);
    shg;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Save calibration results. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fprintf('\nSaving calibration results...\n');
SaveStereoCameraCalibration(outputDir, images, stereoCamera, '/', ...
    optionDisplay);

%[J1, J2] = rectifyStereoImages(I1, I2, stereoParams);