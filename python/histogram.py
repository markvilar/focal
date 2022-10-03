from typing import List

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import cv2
import numpy as np

def plot_histogram(img, bins: int=256, vmin: int=0, vmax: int=255):
    histogram = cv2.calcHist([img], [], None, [bins], [vmin, vmax])

    histogram = np.squeeze(histogram)

    fig = plt.figure(figsize=(3, 3))
    ax1 = fig.add_axes(rect=( 0.05, 0.30, 0.90, 0.65 ))
    ax2 = fig.add_axes(rect=( 0.05, 0.16, 0.90, 0.05 ))

    ax1.plot(histogram, color="0.1")
    ax1.set_ylim([0, 50000])
    ax1.tick_params(left=False, bottom=False, labelleft=False, \
        labelbottom=False)

    sm = plt.cm.ScalarMappable(cmap="gray", \
        norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []

    cb = fig.colorbar(sm, orientation="horizontal", cax=ax2)
    cb.set_ticks([0.0, 64.0, 128.0, 192.0, 255.0])

    return fig

def plot_histogram_rgb(img, vmax: int=256, vmin: int=0, \
    color: List=["r", "g", "b"]):
   
    fig = plt.figure(figsize=(3, 3))
    ax1 = fig.add_axes(rect=( 0.05, 0.30, 0.90, 0.65 ))
    ax2 = fig.add_axes(rect=( 0.05, 0.23, 0.90, 0.05 ))
    ax3 = fig.add_axes(rect=( 0.05, 0.16, 0.90, 0.05 ))
    ax4 = fig.add_axes(rect=( 0.05, 0.09, 0.90, 0.05 ))

    histograms = []
    for i, color in enumerate(color):
        histogram = cv2.calcHist([img], [i], None, [vmax], [vmin, vmax])
        histogram = np.squeeze(histogram)
        histograms.append(histogram)

        ax1.plot(histogram, color=color, linestyle="-")
    

    ax1.set_ylim([0, 50000])

    smr = plt.cm.ScalarMappable(cmap="Reds", \
        norm=plt.Normalize(vmin=vmin, vmax=vmax))
    smr._A = []
    smg = plt.cm.ScalarMappable(cmap="Greens", \
        norm=plt.Normalize(vmin=vmin, vmax=vmax))
    smg._A = []
    smb = plt.cm.ScalarMappable(cmap="Blues", \
        norm=plt.Normalize(vmin=vmin, vmax=vmax))
    smb._A = []

    cb1 = fig.colorbar(smr, orientation="horizontal", cax=ax2)
    cb2 = fig.colorbar(smg, orientation="horizontal", cax=ax3)
    cb3 = fig.colorbar(smb, orientation="horizontal", cax=ax4)

    # Turn off labels
    ax1.tick_params(left=False, bottom=False, labelleft=False, \
        labelbottom=False)
    ax2.tick_params(labelleft=False, labelbottom=False)
    ax3.tick_params(labelleft=False, labelbottom=False)

    cb1.set_ticks([0.0, 64.0, 128.0, 192.0, 255.0])
    cb2.set_ticks([0.0, 64.0, 128.0, 192.0, 255.0])
    cb3.set_ticks([0.0, 64.0, 128.0, 192.0, 255.0])

    return fig

def main():
    raise NotImplementedError

if __name__ == "__main__":
    main()
