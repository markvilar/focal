% Auto-generated by stereoCalibrator app on 01-Mar-2021
%-------------------------------------------------------


% Define images to process
imageFileNames1 = {'/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612888738986-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612888763940-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612888840576-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612888888277-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612888908849-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889001776-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889020542-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889038572-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889060214-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889123336-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889238272-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889270552-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889327886-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889359832-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889404053-left.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/left/1612889406261-left.png',...
    };
imageFileNames2 = {'/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612888738986-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612888763940-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612888840576-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612888888277-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612888908849-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889001776-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889020542-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889038572-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889060214-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889123336-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889238272-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889270552-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889327886-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889359832-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889404053-right.png',...
    '/home/martin/data/tbs-calibration/tbs-calibration-02/subset-03/right/1612889406261-right.png',...
    };

% Detect checkerboards in images
[imagePoints, boardSize, imagesUsed] = detectCheckerboardPoints(imageFileNames1, imageFileNames2);

% Generate world coordinates of the checkerboard keypoints
squareSize = 40;  % in units of 'millimeters'
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% Read one of the images from the first stereo pair
I1 = imread(imageFileNames1{1});
[mrows, ncols, ~] = size(I1);

% Calibrate the camera
[stereoParams, pairsUsed, estimationErrors] = estimateCameraParameters(imagePoints, worldPoints, ...
    'EstimateSkew', false, 'EstimateTangentialDistortion', false, ...
    'NumRadialDistortionCoefficients', 2, 'WorldUnits', 'millimeters', ...
    'InitialIntrinsicMatrix', [], 'InitialRadialDistortion', [], ...
    'ImageSize', [mrows, ncols]);

% View reprojection errors
h1=figure; showReprojectionErrors(stereoParams);

% Visualize pattern locations
h2=figure; showExtrinsics(stereoParams, 'CameraCentric');

% Display parameter estimation errors
displayErrors(estimationErrors, stereoParams);

% You can use the calibration data to rectify stereo images.
I2 = imread(imageFileNames2{1});
[J1, J2] = rectifyStereoImages(I1, I2, stereoParams);

% See additional examples of how to use the calibration data.  At the prompt type:
% showdemo('StereoCalibrationAndSceneReconstructionExample')
% showdemo('DepthEstimationFromStereoVideoExample')