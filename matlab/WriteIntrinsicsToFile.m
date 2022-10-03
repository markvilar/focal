function WriteIntrinsicsToFile(file, intrinsics, errors)
% Writes a set of intrinsic parameters and the corresponding estimation
% errors for the perspective SVP model to a file.
%
% :param file: string, the file path.
% :param intrinsics: cameraIntrinsics object.
% :param errors: intrinsicsEstimationError object.

% Open file.
fileID = fopen(file, 'w');

fprintf(fileID, "Image size: %dx%d\n", intrinsics.ImageSize(2), ...
    intrinsics.ImageSize(1));

% -------------------------------------------------------------------------
% ---- Intrinsic parameters -----------------------------------------------
% -------------------------------------------------------------------------

fprintf(fileID, "\n");
fprintf(fileID, "Focal lengths:           [ %12.6f, %12.6f ]\n", ...
    intrinsics.FocalLength);
fprintf(fileID, "Principal point:         [ %12.6f, %12.6f ]\n", ...
    intrinsics.PrincipalPoint);

if length(intrinsics.RadialDistortion) == 3
fprintf(fileID, "Rad. distortion:         [ %12.6f, %12.6f, %12.6f ]\n", ...
        intrinsics.RadialDistortion);
elseif length(intrinsics.RadialDistortion) == 2
fprintf(fileID, "Rad. distortion:         [ %12.6f, %12.6f ]\n", ...
        intrinsics.RadialDistortion);
end

fprintf(fileID, "Tan. distortion:         [ %12.6f, %12.6f ]\n", ...
    intrinsics.TangentialDistortion);
fprintf(fileID, "Sensor skew:             [ %12.6f ]\n", ...
    intrinsics.Skew);

fprintf(fileID, "\n");
fprintf(fileID, "Camera matrix:\n");
fprintf(fileID, "                         [ %12.6f, %12.6f, %12.6f ]\n", ...
    intrinsics.IntrinsicMatrix);

% -------------------------------------------------------------------------
% ---- Intrinsic errors ---------------------------------------------------
% -------------------------------------------------------------------------

fprintf(fileID, "\n");
fprintf(fileID, "Focal length errors:     [ %12.6f, %12.6f ]\n", ...
    errors.FocalLengthError);
fprintf(fileID, "Principal point errors:  [ %12.6f, %12.6f ]\n", ...
    errors.PrincipalPointError);

if length(errors.RadialDistortionError) == 3
fprintf(fileID, "Rad. distortion errors:  [ %12.6f, %12.6f, %12.6f ]\n", ...
        errors.RadialDistortionError);
elseif length(errors.RadialDistortionError) == 2
fprintf(fileID, "Rad. distortion errors:  [ %12.6f, %12.6f ]\n", ...
        errors.RadialDistortionError);
end

fprintf(fileID, "Tan. distortion errors:  [ %12.6f, %12.6f ]\n", ...
    errors.TangentialDistortionError);
fprintf(fileID, "Sensor skew errors:      [ %12.6f ]\n", ...
    errors.SkewError);

% Close file.
fclose(fileID);
end