from typing import Dict

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

from matplotlib.colors import ListedColormap, LinearSegmentedColormap

plt.style.use("./Styles/Scientific.mplstyle")

import statistics

class CalibrationDataConfiguration:
    def __init__(self, data: Dict, output: str):
        self.data = data
        self.output = output

def plot_reprojection_statistics(config: CalibrationDataConfiguration,
    save_figures: bool=False, show_figures: bool=False):
    """
    Creates various plots of reprojection errors for a given stereo camera 
    calibration.

    :param config: The calibration data and output directory.
    :param save_figures: Save the figures as EPS files.
    :param show_figures: Show the figures during the function call.
    """
    data = config.data

    # Left reprojection errors.
    left_ellipse_scale = 3
    left_errors = np.stack(( data["reprojections-left"]["ErrorX"], \
        data["reprojections-left"]["ErrorY"] ))
    left_mean_error = np.average(left_errors, axis=1)

    fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))
    fig1.tight_layout(pad=2)

    ax1.scatter(left_errors[0, :], left_errors[1, :])
    el1 = statistics.covariance_ellipse(left_errors, ax1, 
        left_ellipse_scale, edgecolor="red", linestyle="--", \
        label=r"3 std. dev.")
    ax1.plot(left_mean_error[0], left_mean_error[1], "r+", markersize=8, \
        label=r"Mean")
    ax1.set_xlim([-3, 3])
    ax1.set_ylim([-3, 3])
    ax1.set_xlabel(r"Reprojection error, $e_{\pi, x}$ $[\text{-}]$")
    ax1.set_ylabel(r"Reprojection error, $e_{\pi, y}$ $[\text{-}]$")

    lg1 = ax1.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1), \
        frameon=True, fancybox=False)
    fr1 = lg1.get_frame()
    fr1.set_facecolor("white")
    fr1.set_edgecolor("black")

    # Right reprojection errors.
    right_ellipse_scale = 3
    right_errors = np.stack(( data["reprojections-right"]["ErrorX"], \
        data["reprojections-right"]["ErrorY"] ))
    right_mean_error = np.average(left_errors, axis=1)

    fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
    fig2.tight_layout(pad=2)

    ax2.scatter(right_errors[0, :], right_errors[1, :])
    el2 = statistics.covariance_ellipse(right_errors, ax2, 
        right_ellipse_scale, edgecolor="red", linestyle="--", \
        label=r"3 std. dev.")
    ax2.plot(right_mean_error[0], right_mean_error[1], "r+", markersize=8, \
        label=r"Mean")
    ax2.set_xlim([-3, 3])
    ax2.set_ylim([-3, 3])
    ax2.set_xlabel(r"Reprojection error, $e_{\pi, x}$ $[\text{-}]$")
    ax2.set_ylabel(r"Reprojection error, $e_{\pi, y}$ $[\text{-}]$")

    lg2 = ax2.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1), \
        frameon=True, fancybox=False)
    fr2 = lg2.get_frame()
    fr2.set_facecolor("white")
    fr2.set_edgecolor("black")

    # Mean reprojection error per image pair.
    left_image_indices = data["reprojections-left"]["Image"].to_numpy()
    left_error_norms = data["reprojections-left"]["ErrorNorm"].to_numpy()
    right_image_indices = data["reprojections-right"]["Image"].to_numpy()
    right_error_norms = data["reprojections-right"]["ErrorNorm"].to_numpy()

    error_norms = np.concatenate( (left_error_norms, right_error_norms) )
    mean_error_norm = np.average(error_norms)
    max_error_norm = np.max(error_norms)

    image_indices = np.unique(left_image_indices)
    image_labels = np.array(image_indices + 1, dtype=object)

    left_mean_error_norms = np.zeros(image_indices.shape)
    right_mean_error_norms = np.zeros(image_indices.shape)
    for index in image_indices:
        left_mean_error_norms[index] = np.average( \
            left_error_norms[left_image_indices == index])
        right_mean_error_norms[index] = np.average( \
            right_error_norms[right_image_indices == index])

    bar_width = 0.2
    bar_spacing = 0.05
    left_bar_positions = image_indices - (bar_width + bar_spacing) / 2
    right_bar_positions = image_indices + (bar_width + bar_spacing) / 2

    # Mean reprojections statistics.
    fig3, ax3 = plt.subplots(figsize=(6.5, 3.5))
    fig3.tight_layout(pad=2, w_pad=2.0, h_pad=2.0)

    ax3.bar(left_bar_positions, left_mean_error_norms, width=0.2, \
        align="edge", label="Left Image")
    ax3.bar(right_bar_positions, right_mean_error_norms, width=0.2, \
        align="edge", label="Right Image")
    ax3.axhline(mean_error_norm, label="Mean Reprojection Error", \
        linestyle="--")
    ax3.set_ylim([0, 1])
    ax3.set_xlabel(r"Image Pair")
    ax3.set_ylabel(r"Reprojection error, $e_{\pi}$ $[-]$")
    ax3.set_xticks(image_indices)
    ax3.set_xticklabels(image_labels)

    lg3 = ax3.legend(loc="upper right", bbox_to_anchor=(1.05, 1.1), \
        frameon=True, fancybox=False)
    fr3 = lg3.get_frame()
    fr3.set_facecolor("white")
    fr3.set_edgecolor("black")

    # Reprojection statistics.
    image_width = data["images"]["Width"][0]
    image_height = data["images"]["Height"][0]
    reprojections_left_x = data["reprojections-left"]["ReprojectedX"]
    reprojections_left_y = data["reprojections-left"]["ReprojectedY"]
    reprojections_right_x = data["reprojections-right"]["ReprojectedX"]
    reprojections_right_y = data["reprojections-right"]["ReprojectedY"]

    colormap = plt.cm.get_cmap("Blues", 256)
    reprojection_colormap = ListedColormap(colormap(np.linspace(0.3, 1.0, 256)))
    reprojection_edgecolor = "none"

    # Reprojections for the left camera. 
    fig4, ax4 = plt.subplots(figsize=(6.5, 3.5))
    fig4.tight_layout(pad=2.2)

    sc4 = ax4.scatter(reprojections_left_x, \
        image_height - reprojections_left_y, c=left_error_norms, \
        vmin=0, vmax=max_error_norm, \
        cmap=reprojection_colormap, edgecolor=reprojection_edgecolor)
    ax4.set_xlim([0, data["images"]["Width"][0]])
    ax4.set_ylim([0, data["images"]["Height"][0]])
    ax4.set_xlabel(r"Reprojected x-coordinate, " \
        + r"$\prescript{u}{}{\hat{x}}$ $[\text{-}]$")
    ax4.set_ylabel(r"Reprojected y-coordinate, " \
        + r"$\prescript{u}{}{\hat{y}}$ $[\text{-}]$")
    
    cb4 = plt.colorbar(sc4, fraction=0.10, pad=0.05)
    cb4.set_label(r"Reprojection error, $e_{\pi}$ $[-]$")

    # Reprojections for the right camera. 
    fig5, ax5 = plt.subplots(figsize=(6.5, 3.5))
    fig5.tight_layout(pad=2.2)

    sc5 = ax5.scatter(reprojections_right_x, \
        image_height - reprojections_right_y, c=right_error_norms, \
        vmin=0, vmax=max_error_norm, \
        cmap=reprojection_colormap, edgecolor=reprojection_edgecolor)
    ax5.set_xlim([0, data["images"]["Width"][0]])
    ax5.set_ylim([0, data["images"]["Height"][0]])
    ax5.set_xlabel(r"Reprojected x-coordinate, " \
        r"$\prescript{u}{}{\hat{x}}$ $[\text{-}]$")
    ax5.set_ylabel(r"Reprojected y-coordinate, " \
        r"$\prescript{u}{}{\hat{y}}$ $[\text{-}]$")

    cb5 = plt.colorbar(sc5, fraction=0.10, pad=0.05)
    cb5.set_label(r"Reprojection error, $e_{\pi}$ $[-]$")

    if save_figures:
        fig1.savefig(config.output + "Reprojection-Errors-Left.pdf", dpi=300)
        fig2.savefig(config.output + "Reprojection-Errors-Right.pdf", dpi=300)
        fig3.savefig(config.output + "Mean-Reprojection-Errors.pdf", dpi=300)
        fig4.savefig(config.output + "Reprojections-Left.pdf", dpi=300)
        fig5.savefig(config.output + "Reprojections-Right.pdf", dpi=300)

    if show_figures:
        plt.show()

def main():
    save_figures = True
    show_figures = True

    dataset_path = "./Data/Calibration-02/"
    output_directory = "./Data/Output/Calibration-Figures/Calibration-02/"

    paths = {}
    paths["images"] = dataset_path + "Calibration-Images.csv"
    paths["target"] = dataset_path + "Calibration-Target.csv"
    paths["extrinsic-errors"] = dataset_path + "Extrinsic-Errors-Left.csv"
    paths["extrinsics-left"]= dataset_path + "Extrinsic-Statistics-Left.csv"
    paths["extrinsics-right"] = dataset_path + "Extrinsic-Statistics-Right.csv"
    paths["reprojections-left"] = dataset_path + \
        "Reprojection-Statistics-Left.csv"
    paths["reprojections-right"] = dataset_path + \
        "Reprojection-Statistics-Right.csv"

    data = {}
    data["images"] = pd.read_csv(paths["images"])
    data["target"] = pd.read_csv(paths["target"])
    data["extrinsic-errors"] = pd.read_csv(paths["extrinsic-errors"])
    data["extrinsics-left"] = pd.read_csv(paths["extrinsics-left"])
    data["extrinsics-right"] = pd.read_csv(paths["extrinsics-right"])
    data["reprojections-left"] = pd.read_csv(paths["reprojections-left"])
    data["reprojections-right"] = pd.read_csv(paths["reprojections-right"])

    config = CalibrationDataConfiguration(data, output_directory)

    plot_reprojection_statistics(config, save_figures, show_figures)

if __name__ == "__main__":
    main()
