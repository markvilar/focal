function SaveStereoCameraCalibration(directory, leftImages, ...
    rightImages, stereoCamera, separator, optionDisplay)
% Undistorts images using the camera model defined by cameraParameters.
% 
% :param directory: string, path to the output directory.
% :param images: ImageDatastore, the image dataset.
% :param stereoCamera: stereoParameters, the stereo camera model.
% :param separator: char, the image file separator.
% :param optionDisplay: bool, display image option.

%% Create directories.
leftUndistortedImageDir = strcat(directory, 'left-undistorted');
leftRectifiedImageDir = strcat(directory, 'left-rectified');
rightUndistortedImageDir = strcat(directory, 'right-undistorted');
rightRectifiedImageDir = strcat(directory, 'right-rectified');

% Create directories.
if ~exist(directory, "dir")
    mkdir(directory);
end
if ~exist(leftUndistortedImageDir, "dir")
    mkdir(leftUndistortedImageDir);
end
if ~exist(leftRectifiedImageDir, "dir")
    mkdir(leftRectifiedImageDir);
end
if ~exist(rightUndistortedImageDir, "dir")
    mkdir(rightUndistortedImageDir);
end
if ~exist(rightRectifiedImageDir, "dir")
    mkdir(rightRectifiedImageDir);
end

assert(length(leftImages.Files) == length(rightImages.Files), ...
    'The number of left and right images are not the same!');

numImagePairs = stereoCamera.NumPatterns;


%% Save images.

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
    
    % Extract image names.
    [leftImageName, extension] = ExtractImageName(leftImages.Files{i}, ...
        separator);
    [rightImageName, ~] = ExtractImageName(rightImages.Files{i}, ...
        separator);
    
    % Load unrectified images.
    leftRawImage = imread(leftImages.Files{i});
    rightRawImage = imread(rightImages.Files{i});
    
    % Undistort images.
    leftUndistortedImage = undistortImage(leftRawImage, ...
        stereoCamera.CameraParameters1);
    rightUndistortedImage = undistortImage(rightRawImage, ...
        stereoCamera.CameraParameters2);
    
    % Rectify images.
    [leftRectifiedImage, rightRectifiedImage] = rectifyStereoImages(...
        leftRawImage, rightRawImage, stereoCamera);
    
    % Show images.
    if (optionDisplay)
        subplot(3, 2, 1);
        imshow(leftRawImage);
        subplot(3, 2, 3);
        imshow(leftUndistortedImage);
        subplot(3, 2, 5);
        imshow(leftRectifiedImage);
        subplot(3, 2, 2);
        imshow(rightRawImage);
        subplot(3, 2, 4);
        imshow(rightUndistortedImage);
        subplot(3, 2, 6);
        imshow(rightRectifiedImage);
        shg;
    end
    
    % Write images.
    imwrite(leftUndistortedImage, strcat(leftUndistortedImageDir, ...
        "/", leftImageName, "-undistorted", ".", extension));
    imwrite(leftRectifiedImage, strcat(leftRectifiedImageDir, ...
        "/", leftImageName, "-rectified", ".", extension));
    imwrite(rightUndistortedImage, strcat(rightUndistortedImageDir, ...
        "/", rightImageName, "-undistorted", ".", extension));
    imwrite(rightRectifiedImage, strcat(rightRectifiedImageDir, ...
        "/", rightImageName, "-rectified", ".", extension));
end

%% Save camera parameters.
fprintf('\n - Saving parameters...');

% Camera intrinsics.
WriteIntrinsicsToFile(strcat(directory, 'intrinsics-left.txt'), ...
    stereoCamera.CameraParameters1.Intrinsics);
WriteIntrinsicsToFile(strcat(directory, 'intrinsics-right.txt'), ...
    stereoCamera.CameraParameters2.Intrinsics);

% Stereo extrinsics.
WriteExtrinsicsToFile(strcat(directory, 'extrinsics.txt'), ...
    stereoCamera);

%% Save reprojection errors.
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