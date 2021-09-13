import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import cv2
import numpy as np

from PIL import Image
from skimage.metrics import structural_similarity as ssim

from histogram import plot_histogram, plot_histogram_rgb

def normalize_image(arr):
    arrmin = np.min(arr)
    arr -= arrmin
    arrmax = np.max(arr)
    arr *= 255.0 / arrmax
    return arr

def save_image(img, path, cmap=None, normalize=None):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap, norm=normalize, resample=False)
    ax.axis("off")
    fig.tight_layout(pad=0.0)
    fig.savefig(path, dpi=300, bbox_inches="tight")

def main():
    img_path = "/home/martin/Data/Example-Images/Image-Color.png"
    img_dl_path = "/home/martin/Data/Example-Images/Image-Color-UIENet.png"

    clahe_clip = 2.0
    clahe_size = 20

    blf_diameter = 10
    blf_color = 60
    blf_space = 20

    # Load images.
    img = cv2.imread(img_path)
    img_uienet = cv2.imread(img_dl_path)

    # Convert color images.
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_img_uienet = cv2.cvtColor(img_uienet, cv2.COLOR_BGR2RGB)

    # Compute gray images.
    img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
    img_uienet = cv2.cvtColor(rgb_img_uienet, cv2.COLOR_RGB2GRAY)

    # Create CLAHE.
    clahe = cv2.createCLAHE(clipLimit=clahe_clip, \
        tileGridSize=(clahe_size, clahe_size))

    # BLF filter.
    img_blf = cv2.bilateralFilter(img, blf_diameter, \
        blf_color, blf_space)
    img_he = cv2.bilateralFilter(cv2.equalizeHist(img), blf_diameter, \
        blf_color, blf_space)
    img_clahe = cv2.bilateralFilter(clahe.apply(img), blf_diameter, \
        blf_color, blf_space)

    # Compute difference image.
    (_, ssi_blf) = ssim(img, img_blf, \
        data_range=img_blf.max() - img_blf.min(), full=True)
    (_, ssi_he) = ssim(img, img_he, \
        data_range=img_he.max() - img_he.min(), full=True)
    (_, ssi_clahe) = ssim(img, img_clahe, \
        data_range=img_clahe.max() - img_clahe.min(), full=True)
    (_, ssi_uienet) = ssim(img, img_uienet, \
        data_range=img_uienet.max() - img_uienet.min(), full=True)

    # Calculate RGB image histograms.
    hist_rgb = plot_histogram_rgb(rgb_img)
    hist_rgb_uienet = plot_histogram_rgb(rgb_img_uienet)

    # Calculate grayscale image histograms.
    hist = plot_histogram(img)
    hist_blf = plot_histogram(img_blf)
    hist_he = plot_histogram(img_he)
    hist_clahe = plot_histogram(img_clahe)
    hist_uienet = plot_histogram(img_uienet)

    hist_rgb.savefig("/home/martin/Data/Images/Histogram-RGB.png", dpi=300)
    hist_rgb_uienet.savefig("/home/martin/Data/Images/Histogram-RGB-UIENet.png", dpi=300)
    hist.savefig("/home/martin/Data/Images/Histogram-Gray.png", dpi=300)
    hist_blf.savefig("/home/martin/Data/Images/Histogram-Gray-BLF.png", dpi=300)
    hist_he.savefig("/home/martin/Data/Images/Histogram-Gray-HE-BLF.png", dpi=300)
    hist_clahe.savefig("/home/martin/Data/Images/Histogram-Gray-CLAHE-BLF.png", dpi=300)
    hist_uienet.savefig("/home/martin/Data/Images/Histogram-Gray-UIENet-BLF.png", dpi=300)

    # Color images.
    save_image(rgb_img, "/home/martin/Data/Images/Image-Color.png")
    save_image(rgb_img_uienet, "/home/martin/Data/Images/Image-Color-UIENet.png")

    # Gray images.
    save_image(img, "/home/martin/Data/Images/Image-Gray.png", "gray")
    save_image(img_blf, "/home/martin/Data/Images/Image-Gray-BLF.png", "gray")
    save_image(img_he, "/home/martin/Data/Images/Image-Gray-HE-BLF.png", "gray")
    save_image(img_clahe, "/home/martin/Data/Images/Image-Gray-CLAHE-BLF.png", "gray")
    save_image(img_uienet, "/home/martin/Data/Images/Image-Gray-UIENet.png", "gray")

    # Difference images.
    save_image(ssi_blf, "/home/martin/Data/Images/Image-SSI-BLF.png", "gray")
    save_image(ssi_he, "/home/martin/Data/Images/Image-SSI-HE-BLF.png", "gray")
    save_image(ssi_clahe, "/home/martin/Data/Images/Image-SSI-CLAHE-BLF.png", "gray")
    save_image(ssi_uienet, "/home/martin/Data/Images/Image-SSI-UIENet.png", "gray")

if __name__ == "__main__":
    main()
