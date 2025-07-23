import numpy as np
from scipy.ndimage import gaussian_filter

def mgn_coronal(image, sigmas=None, weights=None, gamma=3.0, epsilon=1e-3):
    if sigmas is None:
        sigmas = [1.5, 3, 6, 12, 24]
    if weights is None:
        weights = np.ones(len(sigmas)) / len(sigmas)

    stack = []
    for sigma, w in zip(sigmas, weights):
        sm = gaussian_filter(image, sigma)
        lm = gaussian_filter(sm, 1.0)
        ls = np.sqrt(np.maximum(gaussian_filter((sm - lm)**2, 1.0), epsilon))
        norm = (sm - lm) / ls
        tr = np.tanh(gamma * norm)
        stack.append(w * tr)

    return np.sum(stack, axis=0)
