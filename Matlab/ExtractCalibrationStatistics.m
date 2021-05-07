function [reprojectionStatistics, extrinsicStatistics, ...
    targetStatistics] = ExtractCalibrationStatistics(cameraParameters)
% Takes a set of camera parameters, extracts calibration statistics and
% returns them as an array.
%
% :arg cameraParameters: cameraParameters object.
% :return: tuple of arrays, the calibration statistics.

numberOfImages = cameraParameters.NumPatterns;
numberOfPoints = size(cameraParameters.WorldPoints, 1);

% Reprojection statistics.
reprojectionErrors = cameraParameters.ReprojectionErrors;
reprojectedPoints = cameraParameters.ReprojectedPoints;

% Extrinsics statistics.
translationVectors = cameraParameters.TranslationVectors;
rotationVectors = cameraParameters.RotationVectors;

reprojectionStatistics = zeros(numberOfImages*numberOfPoints, 7);
extrinsicStatistics = zeros(numberOfImages, 7);

for i = 1:numberOfImages
    imageErrors = reprojectionErrors(:, :, i);
    imageErrorDistances = sqrt(sum(imageErrors.^2, 2));
    imageReprojections = reprojectedPoints(:, :, i);
    imagePoints = (0:numberOfPoints-1)';
    imageNumbers = repelem(i-1, numberOfPoints)';
    translationVector = translationVectors(i, :);
    rotationVector = rotationVectors(i, :);
    
    offset = (i-1)*numberOfPoints;
    stride = numberOfPoints;
    reprojectionStatistics(offset+1:offset+stride, :) = [imageNumbers, ...
        imagePoints, imageErrors, imageErrorDistances, imageReprojections];
    
    extrinsicStatistics(i, :) = [i-1, translationVector, rotationVector];
end

% Calibration target coordinates.
targetStatistics = [ (0:length(cameraParameters.WorldPoints)-1)'...
    cameraParameters.WorldPoints, ...
    zeros(length(cameraParameters.WorldPoints), 1) ];

% Convert to tables.

reprojectionStatistics = array2table(reprojectionStatistics);
extrinsicStatistics = array2table(extrinsicStatistics);
targetStatistics = array2table(targetStatistics);

reprojectionStatistics.Properties.VariableNames = ...
    [ "Image", "Point", "ErrorX", "ErrorY", "ErrorNorm", ...
    "ReprojectedX", "ReprojectedY" ];
extrinsicStatistics.Properties.VariableNames = ...
    [ "Index", "TranslationX", "TranslationY", "TranslationZ", ...
    "RodriguezAngleX", "RodriguezAngleY", "RodriguezAngleZ"];
targetStatistics.Properties.VariableNames = ...
    [ "Index", "CoordinateX" , "CoordinateY", "CoordinateZ" ];


end