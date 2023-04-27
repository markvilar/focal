INPUT_DIR="/home/martin/data/20221031_skarnsundet"
OUTPUT_DIR="/home/martin/pCloudDrive/data/20221031_skarnsundet"

python src/image_exporter.py \
    --input "$INPUT_DIR/stereo/20221102_142759.svo" \
    --output "$OUTPUT_DIR/images" \
    --start 66000 \
    --stop 100000 \
    --step 15 \
    --stereo
