NAS="/home/martin/pCloudDrive/data/"

python src/image_exporter.py \
    --input "$NAS/20221031_skarnsundet/stereo/20221102_142759.svo" \
    --output "$NAS/20221031_skarnsundet/images" \
    --start 66000 \
    --stop 1000000 \
    --step 15 \
    --stereo
