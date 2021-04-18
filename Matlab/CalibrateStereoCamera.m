function CalibrateStereoCamera(inputDirectory, outputDirectory, ...
    squareSize, units, numberRadialCoefficients, optionTangential, ...
    optionSkew, optionDisplayExtrinsics, optionDisplayImages, ...
    optionSaveImages)

% Suppress warnings.
warning('off','all')

% -------------------------------------------------------------------------
% ---- Image dataloaders --------------------------------------------------
% -------------------------------------------------------------------------

% Set up image dataloaders.
leftImages = imageDatastore(fullfile(inputDirectory, 'left', '*.png'));
rightImages = imageDatastore(fullfile(inputDirectory, 'right', '*.png'));

% Get image sizes.
leftImageSize = [size(readimage(leftImages, 1), 1), ...
    size(readimage(leftImages, 1), 2)];
rightImageSize = [size(readimage(rightImages, 1), 1), ...
    size(readimage(rightImages, 1), 2)];

assert(leftImageSize(1)==rightImageSize(1), "Unequal image heights.");
assert(leftImageSize(2)==rightImageSize(2), "Unequal image widths.");

% -------------------------------------------------------------------------
% ---- Detect checkerboard ------------------------------------------------
% -------------------------------------------------------------------------

% Detect the checkerboards.
fprintf('\nDetecting checkerboard points...');
[imagePoints, boardSize, ~] = detectCheckerboardPoints(...
     leftImages.Files, rightImages.Files);

% Specify world coordinates of checkerboard keypoints.
targetPoints = generateCheckerboardPoints(boardSize, squareSize);

% -------------------------------------------------------------------------
% ---- Calibrate camera ---------------------------------------------------
% -------------------------------------------------------------------------

fprintf('\nCalibrating stereo camera...');
[stereoCamera, usedImages, stereoErrors] = estimateCameraParameters( ...
    imagePoints, targetPoints, ...
    'EstimateSkew', optionSkew, ...
    'EstimateTangentialDistortion', optionTangential, ...
	'NumRadialDistortionCoefficients', numberRadialCoefficients, ...
	'WorldUnits', units, ...
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

fprintf('\nSaving calibration results...');
SaveCalibrationResults(outputDirectory, leftImages, rightImages, ...
    usedImages, stereoCamera, stereoErrors, optionDisplayImages, ...
    optionSaveImages);
end