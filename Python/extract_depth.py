import numpy as np
import pandas as pd
import pyzed.sl as sl

from utilities import progress_bar

def main():
    svo_path = "/home/martin/data/Ekne-Survey/SVO/Ekne-06.svo"
    csv_path = "./Data/Output/Depth-Statistics-Ekne-06.csv"
    time_bias = 54142.715 #51063.171 

    start_frame = 0
    confidence_threshold = 50
    texture_threshold = 90

    init_params = sl.InitParameters(depth_mode=sl.DEPTH_MODE.QUALITY)
    init_params.set_from_svo_file(svo_path)
    init_params.svo_real_time_mode = False
    init_params.coordinate_units = sl.UNIT.METER

    zed = sl.Camera()
    error = zed.open(init_params)
    if not error is sl.ERROR_CODE.SUCCESS:
        sys.std.write(repr(error))
        zed.close()
        exit()

    runtime_params = sl.RuntimeParameters( \
        confidence_threshold=confidence_threshold, \
        texture_confidence_threshold=texture_threshold)

    total_frames = zed.get_svo_number_of_frames()
    zed.set_svo_position(start_frame)

    depth_map = sl.Mat()
    i = 0
    frame = start_frame
    stats = []
    while frame < total_frames:
        if zed.grab(runtime_params) != sl.ERROR_CODE.SUCCESS:
            continue

        i += 1
        frame = zed.get_svo_position()
        zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH, sl.MEM.CPU)
        timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
        time = (timestamp.get_milliseconds() / 1000) + time_bias

        # Filter out invalid values.
        depth_values = depth_map.get_data()
        nan_mask = np.isnan(depth_values)
        inf_mask = np.isinf(depth_values)
        mask = np.logical_not(np.logical_or(nan_mask, inf_mask))

        depth_values = depth_values[mask]

        progress_bar( (frame / total_frames) * 100)

        # Compute statistics.
        depth_mean = np.mean(depth_values)
        depth_std = np.std(depth_values)
        depth_median = np.median(depth_values)
        depth_quantile_91 = np.quantile(depth_values, 0.91)
        depth_quantile_75 = np.quantile(depth_values, 0.75)
        depth_quantile_25 = np.quantile(depth_values, 0.25)
        depth_quantile_09 = np.quantile(depth_values, 0.09)

        stats.append([ time, depth_mean, depth_std, depth_median, \
            depth_quantile_91, depth_quantile_75, depth_quantile_25, \
            depth_quantile_09 ])

    stats = np.array(stats)
    df = pd.DataFrame(stats, columns=["Timestamp", "Mean", "Stddev", "Median", \
        "Quantile-91", "Quantile-75", "Quantile-25", "Quantile-09"])
    df.to_csv(csv_path)

if __name__ == "__main__":
    main()
