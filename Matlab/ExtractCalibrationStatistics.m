function [reprojectionStatistics, extrinsicStatistics] = ...
    ExtractCalibrationStatistics(cameraParameters)
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
    imagePoints = (1:numberOfPoints)';
    imageNumbers = repelem(i, numberOfPoints)';
    translationVector = translationVectors(i, :);
    rotationVector = rotationVectors(i, :);
    
    offset = (i-1)*numberOfPoints;
    stride = numberOfPoints;
    reprojectionStatistics(offset+1:offset+stride, :) = [imageNumbers, ...
        imagePoints, imageErrors, imageErrorDistances, imageReprojections];
    
    extrinsicStatistics(i, :) = [i, translationVector, rotationVector];
end

end