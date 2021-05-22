import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import cv2
from PIL import Image

def main():
    img_path = "./Data/Example-Images/1611262403339.png"
    img_dl_path = "./Data/Example-Images/1611262403339-uienet.png"

    img = cv2.imread(img_path)
    img_corrected = cv2.imread(img_dl_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_corrected = cv2.cvtColor(img_corrected, cv2.COLOR_BGR2RGB)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img_he = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img_clahe = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(20, 20))

    gray_img_he = cv2.equalizeHist(gray_img_he)
    gray_img_clahe = clahe.apply(gray_img_clahe)

    gray_img_filt = cv2.bilateralFilter(gray_img, 7, 60, 20)
    gray_img_he_filt = cv2.bilateralFilter(gray_img_he, 7, 60, 20)
    gray_img_clahe_filt = cv2.bilateralFilter(gray_img_clahe, 7, 60, 20)

    fig1, ax1 = plt.subplots()
    ax1.imshow(img, resample=False)
    ax1.axis("off")

    fig2, ax2 = plt.subplots()
    ax2.imshow(img_corrected, resample=False)
    ax2.axis("off")

    fig3, ax3 = plt.subplots()
    ax3.imshow(gray_img, resample=False, cmap="gray")
    ax3.axis("off")

    fig4, ax4 = plt.subplots()
    ax4.imshow(gray_img_he, resample=False, cmap="gray")
    ax4.axis("off")

    fig5, ax5 = plt.subplots()
    ax5.imshow(gray_img_clahe, resample=False, cmap="gray")
    ax5.axis("off")

    fig6, ax6 = plt.subplots()
    ax6.imshow(gray_img_filt, resample=False, cmap="gray")
    ax6.axis("off")

    fig7, ax7 = plt.subplots()
    ax7.imshow(gray_img_he_filt, resample=False, cmap="gray")
    ax7.axis("off")

    fig8, ax8 = plt.subplots()
    ax8.imshow(gray_img_clahe_filt, resample=False, cmap="gray")
    ax8.axis("off")

    fig1.tight_layout(pad=0.0)
    fig2.tight_layout(pad=0.0)
    fig3.tight_layout(pad=0.0)
    fig4.tight_layout(pad=0.0)
    fig5.tight_layout(pad=0.0)
    fig6.tight_layout(pad=0.0)
    fig7.tight_layout(pad=0.0)
    fig8.tight_layout(pad=0.0)

    fig1.savefig("./Output/Image-Color.pdf", dpi=300, bbox_inches="tight")
    fig2.savefig("./Output/Image-Color-UIENet.pdf", dpi=300, bbox_inches="tight")
    fig3.savefig("./Output/Image-Gray.pdf", dpi=300, bbox_inches="tight")
    fig4.savefig("./Output/Image-Gray-HE.pdf", dpi=300, bbox_inches="tight")
    fig5.savefig("./Output/Image-Gray-CLAHE.pdf", dpi=300, bbox_inches="tight")
    fig6.savefig("./Output/Image-Gray-Filtered.pdf", dpi=300, bbox_inches="tight")
    fig7.savefig("./Output/Image-Gray-Filtered-HE.pdf", dpi=300, bbox_inches="tight")
    fig8.savefig("./Output/Image-Gray-Filtered-CLAHE.pdf", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
