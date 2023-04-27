DATA_DIR="/home/martin/data"

# 20220923_134021.svo - 1080
# 20220923_134431.svo - 1080 (far)
# 20220923_135124.svo - 1080 (far, flip)
# 20220923_140554.svo - 1080 (far, flip)

python python/extract_images.py \
    -i "$DATA_DIR/20220923_134431.svo" \
    -o "$DATA_DIR/1080/" \
    -s 0 \

python python/extract_images.py \
    -i "$DATA_DIR/20220923_135124.svo" \
    -o "$DATA_DIR/1080/" \
    -s 0 \

python python/extract_images.py \
    -i "$DATA_DIR/20220923_140554.svo" \
    -o "$DATA_DIR/1080/" \
    -s 0 \
