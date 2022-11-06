import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim

from histogram import plot_histogram, plot_histogram_rgb

def normalize_image(arr):
    arrmin = np.min(arr)
    arr -= arrmin
    arrmax = np.max(arr)
    arr *= 255.0 / arrmax
    return arr

def compute_similarity_image(image: np.ndarray, reference: np.ndarray):
    diff = image.max() - image.min()
    (_, sim) = ssim(reference, image, data_range=diff, full=True)
    return sim * 255

def show_image(img, cmap=None, normalize=None):
    fig, ax = plt.subplots()
    ax.imshow(img, cmap, norm=normalize, resample=False)
    ax.axis("off")
    fig.tight_layout(pad=0.0)
    return fig, ax

def save_image(img, path):
    cv2.imwrite(path, img)

def main():
    show = False
    save = True

    paths = {}
    paths["Input"] = "/home/martin/Data/Image-Processing/8080.png"
    paths["Output"] = "/home/martin/Data/Image-Processing/"
    prefix = "8080-"

    # BLF parameters.
    blf_size  = 10
    blf_color = 60
    blf_space = 20

    # GF parameters.
    gf_size = 10
    gf_epsilon = 20

    # CLAHE parameters.
    clahe_clip = 2.0
    clahe_size = 20

    # Load images.
    images = {}
    images["Gray"] = cv2.imread(paths["Input"], cv2.IMREAD_GRAYSCALE)

    # Create CLAHE.
    clahe = cv2.createCLAHE(clipLimit=clahe_clip, \
        tileGridSize=(clahe_size, clahe_size))

    # BLF filter.
    images["GF"]    = cv2.ximgproc.guidedFilter(images["Gray"], \
        images["Gray"], gf_size, gf_epsilon)
    images["BLF"]   = cv2.bilateralFilter(images["Gray"], \
        blf_size, blf_color, blf_space)
    images["HE"]    = cv2.equalizeHist(images["Gray"])
    images["CLAHE"] = clahe.apply(images["Gray"])

    # Compute difference image.
    images["SIM-GF"] = compute_similarity_image(images["GF"], images["Gray"])
    images["SIM-BLF"] = compute_similarity_image(images["BLF"], images["Gray"])
    images["SIM-HE"] = compute_similarity_image(images["CLAHE"], images["Gray"])
    images["SIM-CLAHE"] = compute_similarity_image(images["CLAHE"], \
        images["Gray"])

    # Save images.
    if save:
        for key, image in images.items():
            save_image(image, paths["Output"] + prefix + key + ".png")

    if show:
        for key, image in images.items():
            show_image(image, cmap="gray")

        plt.show()

if __name__ == "__main__":
    main()
