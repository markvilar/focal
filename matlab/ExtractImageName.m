function [filename, extension] = ExtractImageName(path, separator)
% Extract the image name and extension from a path.
%
% param path: cell, the file path.
% param separator: char, the file path separator.

path = strsplit(path, separator);
path = string(path(end));
splits = strsplit(path, '.');

filename = splits(1);
extension = splits(2);

end