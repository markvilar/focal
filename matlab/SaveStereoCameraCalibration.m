function SaveStereoCameraCalibration(directory, images, stereoCamera, ...
    separator, optionDisplay)
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

% Split images into left and right images.
leftImages = images.Files(1:2:end, :);
rightImages = images.Files(2:2:end, :);

assert(length(leftImages) == length(rightImages), ...
    'The number of left and right images are not the same!');

% TODO: Save utilized images to txt file.

% Save images.
reverse = '';
numImagePairs = length(leftImages);
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
    [leftImageName, extension] = ExtractImageName(leftImages{i}, ...
        separator);
    
    [rightImageName, ~] = ExtractImageName(leftImages{i}, ...
        separator);
    
    leftUnrectifiedImage = imread(leftImages{i});
    rightUnrectifiedImage = imread(rightImages{i});
    
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
fprintf('\n - Saving camera parameters...');
leftCamera = stereoCamera.CameraParameters1;
rightCamera = stereoCamera.CameraParameters2;
baseline = stereoCamera.TranslationOfCamera2;
rotation = rotm2eul(stereoCamera.RotationOfCamera2, 'XYZ');

fprintf('\nBaseline: %f, %f, %f', baseline(1), baseline(2), baseline(3));
fprintf('\nRotation: %f, %f, %f', rotation(1), rotation(2), rotation(3));

% Save reprojection errors.
fprintf('\n - Saving reprojection errors...\n');
writematrix(permute(stereoCamera.CameraParameters1.ReprojectionErrors, ...
    [3 2 1]), strcat(directory, '/', 'reprojection-errors-left.csv'));
writematrix(permute(stereoCamera.CameraParameters2.ReprojectionErrors, ...
    [3 2 1]), strcat(directory, '/', 'reprojection-errors-right.csv'));
end