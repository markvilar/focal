import matplotlib.patches
import matplotlib.transforms
import numpy as np

def covariance_ellipse(data: np.array, ax, n_std: int=1, facecolor='none',
    **kwargs):
    """
    Parameters
    ----------
    data shape = (2, n)

    Returns
    -------
    CovarianceEllipseParameters
    """

    mean = np.average(data, axis=1)
    covariance = np.cov(data)

    pearson = covariance[0, 1] / np.sqrt(covariance[0, 0] * covariance[1, 1])
    radii = np.array([ np.sqrt(1 + pearson), np.sqrt(1 - pearson) ])

    ellipse = matplotlib.patches.Ellipse((0, 0), width=radii[0] * 2, \
        height=radii[1] * 2, facecolor=facecolor, **kwargs)

    scales = np.array([ np.sqrt(covariance[0, 0]) * n_std, \
        np.sqrt(covariance[1, 1]) * n_std ])

    transform = matplotlib.transforms.Affine2D().rotate(45) \
        .scale(scales[0], scales[1]).translate(mean[0], mean[1])

    ellipse.set_transform(transform + ax.transData)

    return ax.add_patch(ellipse)
