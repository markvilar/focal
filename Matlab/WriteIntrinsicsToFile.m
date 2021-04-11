function WriteIntrinsicsToFile(file, intrinsics)
% Writes a set of intrinsic parameters for the perspective SVP model to a
% file.
%
% :param file: string, the file path.
% :param intrinsics: cameraIntrinsics object, the intrinsic parameters.

intrinsics.FocalLength;
intrinsics.PrincipalPoint;
intrinsics.ImageSize;
intrinsics.RadialDistortion;
intrinsics.TangentialDistortion;
intrinsics.Skew;
intrinsics.IntrinsicMatrix;

% Open file.
fileID = fopen(file, 'w');

fprintf(fileID, "Image size:             %dx%d\n", ...
    intrinsics.ImageSize(2), intrinsics.ImageSize(1));
fprintf(fileID, "Focal lengths:          [ %9.4f, %9.4f ]\n", ...
    intrinsics.FocalLength);
fprintf(fileID, "Principal point:        [ %9.4f, %9.4f ]\n", ...
    intrinsics.PrincipalPoint);

if length(intrinsics.RadialDistortion) == 3
fprintf(fileID, "Radial distortion:      [ %7.4f, %7.4f, %7.4f ]\n", ...
        intrinsics.RadialDistortion);
elseif length(intrinsics.RadialDistortion) == 2
fprintf(fileID, "Radial distortion:      [ %7.4f, %7.4f ]\n", ...
        intrinsics.RadialDistortion);
end

fprintf(fileID, "Tangential distortion:  [ %7.4f, %7.4f ]\n", ...
    intrinsics.TangentialDistortion);
fprintf(fileID, "Image sensor skew:      %6.4f\n", ...
    intrinsics.Skew);
fprintf(fileID, "Camera matrix:\n");
fprintf(fileID, "    [\n");
fprintf(fileID, "        %9.4f, %9.4f, %9.4f\n", ...
    intrinsics.IntrinsicMatrix);
fprintf(fileID, "    ]\n");
% Close file.
fclose(fileID);
end