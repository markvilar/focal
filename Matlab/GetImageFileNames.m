function [imageFileNames] = GetImageFileNames(directory, separator, extension)
% Returns the name of image files of a given extension.
assert(isa(directory, 'char'), "Input directory must be a char.");
files = dir([directory separator '*.' extension]);

imageFileNames = cell(size(files));
for i=1:length(files)
    imageFileNames{i} = [files(i).folder separator files(i).name];
end
end