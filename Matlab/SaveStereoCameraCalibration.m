function SaveStereoCameraCalibration(directory, leftImages, ...
    rightImages, stereoCamera, separator, optionDisplay)
% Undistorts images using the camera model defined by cameraParameters.
% 
% :param directory: string, path to the output directory.
% :param images: ImageDatastore, the image dataset.
% :param stereoCamera: stereoParameters, the stereo camera model.
% :param separator: char, the image file separator.
% :param optionDisplay: bool, display image option.

leftUnrectifiedImageDir = strcat(directory, 'left-unrectified');
leftRectifiedImageDir = strcat(directory, 'left-rectified');
rightUnrectifiedImageDir = strcat(directory, 'right-unrectified');
rightRectifiedImageDir = strcat(directory, 'right-rectified');

% Create directories.
if ~exist(directory, "dir")
    mkdir(directory);
end
if ~exist(leftUnrectifiedImageDir, "dir")
    mkdir(leftUnrectifiedImageDir);
end
if ~exist(leftRectifiedImageDir, "dir")
    mkdir(leftRectifiedImageDir);
end
if ~exist(rightUnrectifiedImageDir, "dir")
    mkdir(rightUnrectifiedImageDir);
end
if ~exist(rightRectifiedImageDir, "dir")
    mkdir(rightRectifiedImageDir);
end

assert(length(leftImages.Files) == length(rightImages.Files), ...
    'The number of left and right images are not the same!');

numImagePairs = stereoCamera.NumPatterns;

% TODO: Save utilized images to txt file.

reverse = '';

if (optionDisplay)
    figure;
end

for i=1:numImagePairs
    % Progress bar.
    percent = 100 * i / numImagePairs;
    message = sprintf(' - Saving images, percentage: %3.1f', percent);
    fprintf([reverse, message]);
    reverse = repmat(sprintf('\b'), 1, length(message));
    
    % Load and undistort image.
    [leftImageName, extension] = ExtractImageName(leftImages.Files{i}, ...
        separator);
    
    [rightImageName, ~] = ExtractImageName(rightImages.Files{i}, ...
        separator);
    
    leftUnrectifiedImage = imread(leftImages.Files{i});
    rightUnrectifiedImage = imread(rightImages.Files{i});
    
    % Rectify images.
    leftRectifiedImage = undistortImage(leftUnrectifiedImage, ...
        stereoCamera.CameraParameters1);
    rightRectifiedImage = undistortImage(rightUnrectifiedImage, ...
        stereoCamera.CameraParameters2);
    
    % Show images.
    if (optionDisplay)
        subplot(2, 2, 1);
        imshow(leftUnrectifiedImage);
        subplot(2, 2, 3);
        imshow(leftRectifiedImage);
        subplot(2, 2, 2);
        imshow(rightUnrectifiedImage);
        subplot(2, 2, 4);
        imshow(rightRectifiedImage);
    end
    
    % Format image file names.
    leftUnrectifiedImageName = strcat(leftImageName, '-unrectified', ...
        '.', extension);
    leftRectifiedImageName = strcat(leftImageName, '-rectified', ...
        '.', extension);
    rightUnrectifiedImageName = strcat(rightImageName, '-unrectified', ...
        '.', extension);
    rightRectifiedImageName = strcat(rightImageName, '-rectified', ...
        '.', extension);
    
    % Write images.
    imwrite(leftUnrectifiedImage, strcat(leftUnrectifiedImageDir, ...
        '/', leftUnrectifiedImageName));
    imwrite(leftRectifiedImage, strcat(leftRectifiedImageDir, ...
        '/', leftRectifiedImageName));
    imwrite(rightUnrectifiedImage, strcat(rightUnrectifiedImageDir, ...
        '/', rightUnrectifiedImageName));
    imwrite(rightRectifiedImage, strcat(rightRectifiedImageDir, ...
        '/', rightRectifiedImageName));
end

% Save camera parameters.
fprintf('\n - Saving parameters...');
baseline = stereoCamera.TranslationOfCamera2;
rotation = rotm2eul(stereoCamera.RotationOfCamera2, 'XYZ');

fprintf('\n    - Baseline: %f, %f, %f', baseline(1), baseline(2), ...
    baseline(3));
fprintf('\n    - Rotation: %f, %f, %f', rotation(1), rotation(2), ...
    rotation(3));

% Save reprojection errors.
fprintf('\n - Saving statistics...\n');

[leftReprojectionStatistics, leftExtrinsicStatistics] = ...
    ExtractCalibrationStatistics(stereoCamera.CameraParameters1);
[rightReprojectionStatistics, rightExtrinsicStatistics] = ...
    ExtractCalibrationStatistics(stereoCamera.CameraParameters2);

writematrix(leftReprojectionStatistics, ...
    strcat(directory, 'reprojection-statistics-left.csv'));
writematrix(leftExtrinsicStatistics, ...
    strcat(directory, 'extrinsic-statistics-left.csv'));
writematrix(rightReprojectionStatistics, ...
    strcat(directory, 'reprojection-statistics-right.csv'));
writematrix(rightExtrinsicStatistics, ...
    strcat(directory, 'extrinsic-statistics-right.csv'));
end