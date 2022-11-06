import cv2
import matplotlib.pyplot as plt

from dataloaders import SVODataloader

def main():
    path = "/home/martin/Data/Stereo/SVO/Ekne-01.svo"
    stop = False

    loader = SVODataloader()
    loader.load(path)
    loader.set_index(5000)

    blf_diameter = 7
    blf_sigmar = 20
    blf_sigmas = 20

    detect_length     = 50
    detect_distance   = 30
    detect_canny_low  = 10
    detect_canny_high = 20
    detect_aperture   = 7
    detect_merge      = True

    detector = cv2.ximgproc.createFastLineDetector(
        detect_length,
        detect_distance,
        detect_canny_low,
        detect_canny_high,
        detect_aperture,
        detect_merge)

    image = {}
    image["Left"] = {}
    image["Right"] = {}
    while loader.has_image() and not stop:
        (time, image["Left"]["Raw"], image["Right"]["Raw"]) = loader.get_frame()

        # Apply BL filter.
        image["Left"]["Processed"] = cv2.bilateralFilter( \
            image["Left"]["Raw"], blf_diameter, blf_sigmar, blf_sigmas)
        image["Right"]["Processed"] = cv2.bilateralFilter( \
            image["Right"]["Raw"], blf_diameter, blf_sigmar, blf_sigmas)

        # Detect line features.
        left_lines = detector.detect(image["Left"]["Processed"])
        right_lines = detector.detect(image["Right"]["Processed"])

        image["Left"]["Lines"] = detector.drawSegments( \
            image["Left"]["Processed"], left_lines)
        image["Right"]["Lines"] = detector.drawSegments( \
            image["Right"]["Processed"], right_lines)

        cv2.imshow("Left", image["Left"]["Lines"])
        key = cv2.waitKey(10)

        if key == 27:
            stop = True

if __name__ == "__main__":
    main()
