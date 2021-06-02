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
    img_path = "/home/martin/Data/Example-Images/1611262403339.png"
    img_dl_path = "/home/martin/Data/Example-Images/1611262403339-uienet.png"

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

    hist_rgb.savefig("./Data/Output/Histogram-RGB.pdf", dpi=300)
    hist_rgb_uienet.savefig("./Data/Output/Histogram-RGB-UIENet.pdf", dpi=300)
    hist.savefig("./Data/Output/Histogram-Gray.pdf", dpi=300)
    hist_blf.savefig("./Data/Output/Histogram-Gray-BLF.pdf", dpi=300)
    hist_he.savefig("./Data/Output/Histogram-Gray-HE-BLF.pdf", dpi=300)
    hist_clahe.savefig("./Data/Output/Histogram-Gray-CLAHE-BLF.pdf", dpi=300)
    hist_uienet.savefig("./Data/Output/Histogram-Gray-UIENet-BLF.pdf", dpi=300)

    # Color images.
    save_image(rgb_img, "./Data/Output/Image-Color.pdf")
    save_image(rgb_img_uienet, "./Data/Output/Image-Color-UIENet.pdf")

    # Gray images.
    save_image(img, "./Data/Output/Image-Gray.pdf", "gray")
    save_image(img_blf, "./Data/Output/Image-Gray-BLF.pdf", "gray")
    save_image(img_he, "./Data/Output/Image-Gray-HE-BLF.pdf", "gray")
    save_image(img_clahe, "./Data/Output/Image-Gray-CLAHE-BLF.pdf", "gray")
    save_image(img_uienet, "./Data/Output/Image-Gray-UIENet.pdf", "gray")

    # Difference images.
    save_image(ssi_blf, "./Data/Output/Image-SSI-BLF.pdf", "gray")
    save_image(ssi_he, "./Data/Output/Image-SSI-HE-BLF.pdf", "gray")
    save_image(ssi_clahe, "./Data/Output/Image-SSI-CLAHE-BLF.pdf", "gray")
    save_image(ssi_uienet, "./Data/Output/Image-SSI-UIENet.pdf", "gray")

if __name__ == "__main__":
    main()
