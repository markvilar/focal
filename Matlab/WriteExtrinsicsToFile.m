function WriteExtrinsicsToFile(file, extrinsics)
% 
% :param file: string, the file path.
% :param extrinsics: stereoParameters, the extrinsic parameters.

% Open file.
fileID = fopen(file, 'w');

fprintf(fileID, "Baseline vector:     [ %9.4f, %9.4f, %9.4f ]\n", ...
    extrinsics.TranslationOfCamera2);
fprintf(fileID, "Rotation, Euler XYZ: [ %9.4f, %9.4f, %9.4f ]\n", ...
    rotm2eul(extrinsics.RotationOfCamera2, "XYZ"));
fprintf(fileID, "Rotation matrix:\n");
fprintf(fileID, "    [\n");
fprintf(fileID, "        %6.4f, %6.4f, %6.4f \n", ...
    extrinsics.RotationOfCamera2);
fprintf(fileID, "    ]\n");
fprintf(fileID, "Essential matrix:\n");
fprintf(fileID, "    [\n");
fprintf(fileID, "        %10.4f, %10.4f, %10.4f \n", ...
    extrinsics.EssentialMatrix);
fprintf(fileID, "    ]\n");
fprintf(fileID, "Fundamental matrix:\n");
fprintf(fileID, "    [\n");
fprintf(fileID, "        %10.4f, %10.4f, %10.4f \n", ...
    extrinsics.FundamentalMatrix);
fprintf(fileID, "    ]\n");

% Close file.
fclose(fileID);
end