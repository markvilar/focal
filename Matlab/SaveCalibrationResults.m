function SaveCalibrationResults(directory, leftImages, rightImages, ...
    usedImages, stereoCamera, optionDisplay)
% Undistorts images using the camera model defined by cameraParameters.
% 
% :param directory: string, path to the output directory.
% :param leftImages: ImageDatastore, the left images.
% :param rightImages: ImageDatastore, the right images.
% :param usedImages: boolean array, the images used for calibration.
% :param stereoCamera: stereoParameters, the stereo camera model.
% :param optionDisplay: bool, display image option.

%% Save images.
fprintf('\n - Saving images...');

WriteImagesToFile(directory, leftImages, rightImages, usedImages, ...
    stereoCamera, optionDisplay);

%% Save camera parameters.
fprintf('\n - Saving parameters...');

% Camera intrinsics.
WriteIntrinsicsToFile( ...
    strcat(directory, 'Intrinsic-Parameters-Left.txt'), ...
    stereoCamera.CameraParameters1.Intrinsics);
WriteIntrinsicsToFile( ...
    strcat(directory, 'Intrinsic-Parameters-Right.txt'), ...
    stereoCamera.CameraParameters2.Intrinsics);

% Stereo extrinsics.
WriteExtrinsicsToFile(strcat(directory, 'Extrinsic-Parameters.txt'), ...
    stereoCamera);

%% Save reprojection errors and calibration target statistics.
fprintf('\n - Saving statistics...\n');

[leftReprojectionStats, leftExtrinsicsStats, targetCoordinates] = ...
    ExtractCalibrationStatistics(stereoCamera.CameraParameters1);
[rightReprojectionStats, rightExtrinsicStats, ~] = ...
    ExtractCalibrationStatistics(stereoCamera.CameraParameters2);

writetable(targetCoordinates, ...
    strcat(directory, "Calibration-Target.csv"));
writetable(leftReprojectionStats, ...
    strcat(directory, 'Reprojection-Statistics-Left.csv'));
writetable(rightReprojectionStats, ...
    strcat(directory, 'Reprojection-Statistics-Right.csv'));
writetable(leftExtrinsicsStats, ...
    strcat(directory, 'Extrinsic-Statistics-Left.csv'));
writetable(rightExtrinsicStats, ...
    strcat(directory, 'Extrinsic-Statistics-Right.csv'));
end