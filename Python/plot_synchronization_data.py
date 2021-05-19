import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np

def main():
    dive1 = np.array([
        [ 1611262305.295, 1611313362.010 ],
        [ 1611262334.029, 1611313391.331 ],
        [ 1611262594.877, 1611313651.458 ],
        [ 1611262619.597, 1611313676.833 ],
        [ 1611262668.501, 1611313725.958 ],
        [ 1611263025.684, 1611314083.080 ],
        [ 1611263194.408, 1611314251.920 ] ])
    
    dive2 = np.array([
        [ 1611261941.868, 1611316083.500 ],
        [ 1611261957.088, 1611316099.077 ],
        [ 1611262086.175, 1611316228.346 ],
        [ 1611262120.829, 1611316262.520 ],
        [ 1611262192.079, 1611316333.808 ],
        [ 1611262305.409, 1611316447.600 ],
        [ 1611262329.728, 1611316471.520 ],
        [ 1611262413.588, 1611316556.120 ],
        [ 1611262557.492, 1611316700.000 ],
        [ 1611262572.277, 1611316714.480 ],
        [ 1611262591.310, 1611316733.385 ],
        [ 1611262622.988, 1611316765.520 ],
        [ 1611262661.690, 1611316803.654 ] ])

    time1 = dive1[:, 1]
    time2 = dive2[:, 1]
    bias1 = dive1[:, 1] - dive1[:, 0]
    bias2 = dive2[:, 1] - dive2[:, 0]
    mean1 = np.average(bias1)
    mean2 = np.average(bias2)
    std1 = np.std(bias1)
    std2 = np.std(bias2)

    fig1, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(7, 3.0))
    fig1.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)

    ax1[0].axhline(mean1, linestyle="-", color="b")
    ax1[0].axhline(mean1 + std1, label=r"Mean $\pm$ std. dev.", linestyle="--", \
        color="b")
    ax1[0].axhline(mean1 - std1, linestyle="--", color="b")
    ax1[0].scatter(time1, bias1, label="Samples")
    ax1[0].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[0].set_ylabel(r"Bias, dive 1, $t_{b}$ $[\text{s}]$")
    ax1[0].set_ylim([ 51056.3, 51058.3 ])

    ax1[1].axhline(mean2, linestyle="-", color="b")
    ax1[1].axhline(mean2 + std2, linestyle="--", color="b")
    ax1[1].axhline(mean2 - std2, linestyle="--", color="b")
    ax1[1].scatter(time2, bias2)
    ax1[1].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[1].set_ylabel(r"Bias, dive 2, $t_{b}$ $[\text{s}]$")
    ax1[1].set_ylim([ 54141, 54143 ])

    lg1 = fig1.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0), \
        frameon=True, fancybox=False)
    fr1 = lg1.get_frame()
    fr1.set_facecolor("white")
    fr1.set_edgecolor("black")

    fig1.savefig("/home/martin/dev/Focal/Output/Synchronization-Points.pdf", \
        dpi=300)
  
    plt.show()

if __name__ == "__main__":
    main()
