function WriteExtrinsicsToFile(file, extrinsics, errors)
% 
% :param file: string, the file path.
% :param extrinsics: stereoParameters object.
% :param errors: stereoErrors object.

% Open file.
fileID = fopen(file, 'w');

fprintf(fileID, "Rotations are defined as the rotation of the right \n");
fprintf(fileID, "camera (camera 2) with respect to the left camera \n");
fprintf(fileID, "(camera 1). Rotation vectors are Rodrigues vectors. \n");

fprintf(fileID, "\n");
fprintf(fileID, "Units: %s\n", extrinsics.WorldUnits);

fprintf(fileID, "\n");
fprintf(fileID, "Baseline vector:     [ %15.10f, %15.10f, %15.10f ]\n", ...
    extrinsics.TranslationOfCamera2);
fprintf(fileID, "Rotation vector:     [ %15.10f, %15.10f, %15.10f ]\n", ...
    rotationMatrixToVector(extrinsics.RotationOfCamera2));

fprintf(fileID, "\nRotation matrix:\n");
fprintf(fileID, "                     [ %15.10f, %15.10f, %15.10f ]\n", ...
    extrinsics.RotationOfCamera2);

fprintf(fileID, "\nEssential matrix:\n");
fprintf(fileID, "                     [ %15.10f, %15.10f, %15.10f ]\n", ...
    extrinsics.EssentialMatrix);

fprintf(fileID, "\nFundamental matrix:\n");
fprintf(fileID, "                     [ %15.10f, %15.10f, %15.10f ]\n", ...
    extrinsics.FundamentalMatrix);

fprintf(fileID, "\n");
fprintf(fileID, "Baseline errors:     [ %15.10f, %15.10f, %15.10f ]\n", ...
    errors.TranslationOfCamera2Error);
fprintf(fileID, "Rotation errors:     [ %15.10f, %15.10f, %15.10f ]\n", ...
    errors.RotationOfCamera2Error);

% Close file.
fclose(fileID);
end