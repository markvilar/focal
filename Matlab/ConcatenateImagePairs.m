clear;
clc;

inputDirectory = strcat("/home/martin/data/Calibration-Experiments/",
    "Calibration-Images-01");

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

numberOfImagePairs = length(leftImages.Files);

for i = 1:numberOfImagePairs
    leftImagePath = leftImages.Files{i};
    rightImagePath = rightImages.Files{i};
    
    [leftImageName, extension] = ExtractImageName(leftImagePath, '/');
    
    imageName = strsplit(leftImageName, '-');
    imageName = imageName(1);
    
    leftImage = imread(leftImagePath);
    rightImage = imread(rightImagePath);
    
    stereoImage = [leftImage, rightImage];
    imwrite(stereoImage, strcat(inputDirectory, imageName, '.', ...
        extension));
end