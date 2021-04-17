function WriteImagesToFile(directory, leftImages, rightImages, ...
    usedImages, stereoCamera, optionDisplay)
% Writes the name of a set of stereo image pairs to a file.
%
% :param directory: string, the root directory path.
% :param leftImages: ImageDatastore object, the left camera images.
% :param rightImages: ImageDatastore object, the right camera images.
% :param stereoCamera: stereoParameters object, the stereo parameters.
% :param optionDisplay: bool, whether or not to display images.

%% Create directories.
leftUndistortedImageDir = strcat(directory, "left-undistorted");
leftRectifiedImageDir = strcat(directory, "left-rectified");
rightUndistortedImageDir = strcat(directory, "right-undistorted");
rightRectifiedImageDir = strcat(directory, "right-rectified");

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
    "The number of left and right images are not the same!");

numImagePairs = stereoCamera.NumPatterns;

%% Save image names utilized for the calibration.

imageStatistics = [num2cell(usedImages), leftImages.Files, rightImages.Files];

for i=1:numImagePairs
    leftImagePath = strsplit(imageStatistics{i, 2}, '/');
    rightImagePath = strsplit(imageStatistics{i, 3}, '/');
    imageStatistics(i, 2) = leftImagePath(end);
    imageStatistics(i, 3) = rightImagePath(end);
end

imageTable = cell2table(imageStatistics);
imageTable.Properties.VariableNames = [ "Used", "ImageLeft", ...
    "ImageRight" ];
writetable(imageTable, strcat(directory, "Calibration-Images.csv"));

%% Save undistorted and rectified images.

reverse = '';

if (optionDisplay)
    figure;
end

for i=1:numImagePairs
    % Progress bar.
    percent = 100 * i / numImagePairs;
    message = sprintf(' %3.1f / 100', percent);
    fprintf([reverse, message]);
    reverse = repmat(sprintf('\b'), 1, length(message));
    
    % Extract image names.
    [leftImageName, extension] = ExtractImageName(leftImages.Files{i}, ...
        '/');
    [rightImageName, ~] = ExtractImageName(rightImages.Files{i}, '/');
    
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
end