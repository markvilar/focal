import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import cv2

def main():
    path = "/home/martin/data/Calibration-Experiments/Experiment-01/Left/" \
        + "1612888950190-left.png"
    # 1612888732095-left.png
    hist_size = 256
    hist_lims = (0, 256)
    accumulate = False

    print(path)

    img = cv2.imread(path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    histogram = cv2.calcHist(gray_img, [0], None, [hist_size], hist_lims, 
        accumulate=accumulate)

    print(type(histogram))

    cv2.imshow("Original", img)
    cv2.imshow("Histogram", histogram)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
