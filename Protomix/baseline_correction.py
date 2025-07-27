import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import factorized, spsolve


def als(y, smoothness=10e4, asymmetry=10e-6, max_iter=100):
    """
    Asymmetric Least Squares (ALS) baseline correction.

    Parameters:
        y (array-like): Input spectrum (1D).
        smoothness (float): Smoothing strength (λ).
        asymmetry (float): Asymmetry parameter (p).
        max_iter (int): Maximum number of iterations.

    Returns:
        ndarray: Baseline-corrected signal.
    """
    y = np.asarray(y)
    m = len(y)
    D = sparse.eye(m, format='csc')
    D = D[1:] - D[:-1]
    D = D[1:] - D[:-1]
    D = D.T
    w = np.ones(m)

    for _ in range(max_iter):
        W = sparse.diags(w, 0, shape=(m, m))
        Z = W + smoothness * D @ D.T
        z = spsolve(Z, w * y)
        w = asymmetry * (y > z) + (1 - asymmetry) * (y < z)

    return y - z

def arpls(y, smoothness=10e2, tolerance=0.05, max_iter=100):
    """
    Adaptive Reweighted Penalized Least Squares (arPLS) baseline correction.

    Parameters:
        y (array-like): Input spectrum (1D).
        smoothness (float): Smoothing strength (λ).
        tolerance (float): Convergence threshold.
        max_iter (int): Maximum number of iterations.

    Returns:
        ndarray: Baseline-corrected signal.
    """
    y = np.asarray(y)
    N = len(y)

    D = sparse.eye(N, format='csc')
    D = D[1:] - D[:-1]
    D = D[1:] - D[:-1]  # Second-order difference matrix
    H = smoothness * (D.T @ D)

    w = np.ones(N)

    for _ in range(max_iter):
        W = sparse.diags(w, 0, shape=(N, N))
        WH = W + H
        solver = factorized(WH)
        z = solver(w * y)

        d = y - z
        dn = d[d < 0]
        m = np.mean(dn)
        s = np.std(dn)

        if s == 0 or np.isnan(s):
            break

        wt = 1.0 / (1 + np.exp(2 * (d - (2 * s - m)) / s))
        if np.linalg.norm(w - wt) / np.linalg.norm(w) < tolerance:
            break
        w = wt

    return y - z

def WhittakerSmooth(x, w, smoothness, diff_order=1):
    """
    Whittaker smoother using sparse linear system.

    Parameters:
        x (array-like): Input signal.
        w (array-like): Weight vector.
        smoothness (float): Smoothing parameter λ.
        diff_order (int): Order of finite differences.

    Returns:
        ndarray: Smoothed signal.
    """
    x = np.asarray(x)
    m = len(x)
    D = sparse.eye(m, format='csc')
    for _ in range(diff_order):
        D = D[1:] - D[:-1]
    W = sparse.diags(w, 0, shape=(m, m))
    A = W + smoothness * D.T @ D
    B = W @ x
    background = spsolve(A, B)
    return background

def airpls(x, smoothness=10e4, diff_order=1, max_iter=100):
    """
    Adaptive Iteratively Reweighted Penalized Least Squares (airPLS) baseline correction.

    Parameters:
        x (array-like): Input spectrum (1D).
        smoothness (float): Smoothing strength (λ).
        diff_order (int): Order of difference matrix.
        max_iter (int): Maximum number of iterations.

    Returns:
        ndarray: Baseline-corrected signal.
    """
    x = np.asarray(x)
    m = x.shape[0]
    w = np.ones(m)

    for i in range(1, max_iter + 1):
        z = WhittakerSmooth(x, w, smoothness, diff_order)
        d = x - z
        dssn = np.abs(d[d < 0].sum())
        if dssn < 0.001 * np.abs(x).sum() or i == max_iter:
            if i == max_iter:
                print("airPLS: max iteration reached.")
            break
        w[d >= 0] = 0
        w[d < 0] = np.exp(i * np.abs(d[d < 0]) / dssn)
        w[0] = w[-1] = np.exp(i * np.max(d[d < 0]) / dssn)
    return x - z

def baseline_correction(
    spectra_df: pd.DataFrame,
    method="arpls",
) -> pd.DataFrame:
    """
    Apply baseline correction to a DataFrame of spectra using selected method.

    Parameters:
        spectra (pd.DataFrame): Rows = spectra, columns = x-axis (e.g., chemical shift).
        method (str): 'arpls', 'als', or 'airpls'.
        smoothness (float): Smoothing parameter (λ).
        tolerance (float): Convergence threshold (used for arPLS).
        max_iter (int): Maximum iterations.
        asymmetry (float): Asymmetry parameter for ALS.
        diff_order (int): Difference order (for airPLS and Whittaker).

    Returns:
        pd.DataFrame: Baseline-corrected spectra.
    """
    if method == "arpls":
        corrected = spectra_df.apply(lambda row: arpls(row, smoothness=10e2, tolerance=0.05, max_iter=100), axis=1)
    elif method == "airpls":
        corrected = spectra_df.apply(lambda row: airpls(row, smoothness=10e4, diff_order=1, max_iter=100), axis=1)
    elif method == "als":
        corrected = spectra_df.apply(lambda row: als(row, smoothness=10e4, asymmetry=10e-6, max_iter=100), axis=1)
    else:
        raise ValueError("Method must be one of: 'arpls', 'als', 'airpls'.")

    corrected_array = np.vstack(corrected.values)
    return pd.DataFrame(corrected_array, index=spectra_df.index, columns=spectra_df.columns)