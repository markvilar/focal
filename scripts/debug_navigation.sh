#!/usr/bin/bash

DATA_DIR="/home/martin/data"

python src/navigation_exporter.py --logs \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_091526_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_101527_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_111528_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_121529_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_131530_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_142305_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_152306_S.NPD" \
    "$DATA_DIR/20221031_skarnsundet/navigation/20221102_162307_S.NPD"
