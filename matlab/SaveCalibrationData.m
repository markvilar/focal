function SaveCalibrationData(directory, files, parameters, errors, ...
    separator)
% Undistorts images using the camera model defined by cameraParameters.
% 
% :param directory: string, path to the output directory.
% :param files: cell array of strings, paths to the images.
% :param parameters: object, the calibration parameters.
% :param errors: object, the calibration errors.
% :param separator: char, the.

if ~exist(directory, "dir")
    mkdir(directory);
end

for i=1:length(files)
    % Load and undistort image.
    filename = strsplit(files{i}, separator);
    filename = filename(end);
    filename = strsplit(filename, '.');
    image = imread(files{i});
    undistortedImage = undistortImage(image, parameters);
    
    % Plot.
    subplot(1, 2, 1);
    imshow(image);
    subplot(1, 2, 2);
    imshow(undistortedImage);
    
    % Save to file.
    
end

end