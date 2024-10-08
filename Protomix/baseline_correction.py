import numpy as np
import pandas as pd

from scipy import sparse
from scipy.sparse.linalg import spsolve

def baseline_correction(spectra_df: pd.DataFrame, method="als", lambda_=100, porder=1, maxIter=100, lam=1e4, ratio=0.05):
    """
    Apply different baseline correction algorithms to each row of a DataFrame.

    :param spectra_df: DataFrame where each row is a spectrum to be baseline corrected.
    :type spectra_df: pd.DataFrame
    :param method: Method for baseline correction. Options are "als", "arpls", "airpls".
    :type method: str
    :param lambda_: Regularization parameter for ALS and AIRPLS.
    :type lambda_: float
    :param porder: Asymmetry parameter for ALS.
    :type porder: float
    :param maxIter: Maximum number of iterations for ALS and AIRPLS.
    :type maxIter: int
    :param lam: Lambda parameter for ARPLS.
    :type lam: float
    :param ratio: Ratio parameter for ARPLS.
    :type ratio: float
    
    :return: DataFrame with baseline corrected spectra.
    :rtype: pd.DataFrame
    """

    if method == "als":
        corrected_spectra_df = spectra_df.apply(lambda row: als(row, lambda_, porder, maxIter), axis=1)
    elif method == "arpls":
        corrected_spectra_df = spectra_df.apply(lambda row: arpls(row, lam, ratio), axis=1)
    elif method == "airpls":
        corrected_spectra_df = spectra_df.apply(lambda row: airpls(row, lambda_, porder, maxIter), axis=1)
    else:
        raise ValueError("Invalid method. Supported methods: 'als', 'arpls', 'airpls'")
    
    return pd.DataFrame(corrected_spectra_df)


def als(y, lambda_, p, maxIter):
    m = len(y)
    D = sparse.eye(m, format='csc')
    D = D[1:] - D[:-1]  # numpy.diff( ,2) does not work with sparse matrix. This is a workaround.
    D = D[1:] - D[:-1]
    D = D.T
    w = np.ones(m)
    for i in range(maxIter):
        W = sparse.diags(w, 0, shape=(m, m))
        Z = W + lambda_ * D.dot(D.T)
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return y - z

def arpls(y, lam=1e4, ratio=0.05, itermax=100):
    N = len(y)
    # D = sparse.csc_matrix(np.diff(np.eye(N), 2))
    D = sparse.eye(N, format='csc')
    D = D[1:] - D[:-1]  # numpy.diff( ,2) does not work with sparse matrix. This is a workaround.
    D = D[1:] - D[:-1]

    H = lam * D.T * D
    w = np.ones(N)
    for i in range(itermax):
        W = sparse.diags(w, 0, shape=(N, N))
        WH = sparse.csc_matrix(W + H)
        C = sparse.csc_matrix(cholesky(WH.todense()))
        z = spsolve(C, spsolve(C.T, w * y))
        d = y - z
        dn = d[d < 0]
        m = np.mean(dn)
        s = np.std(dn)
        wt = 1. / (1 + np.exp(2 * (d - (2 * s - m)) / s))
        if np.linalg.norm(w - wt) / np.linalg.norm(w) < ratio:
            break
        w = wt
    return y - z


def WhittakerSmooth(x, w, lam, differences=1):
    X = np.matrix(x)
    m = X.size
    # D = csc_matrix(np.diff(np.eye(m), differences))
    D = sparse.eye(m, format='csc')
    for i in range(differences):
        D = D[1:] - D[:-1]  # numpy.diff() does not work with sparse matrix. This is a workaround.
    W = sparse.diags(w, 0, shape=(m, m))
    A = sparse.csc_matrix(W + (lam * D.T * D))
    B = sparse.csc_matrix(W * X.T)
    background = spsolve(A, B)
    return np.array(background)

def airpls(x, lambda_=100, porder=1, maxIter=100):
    m = x.shape[0]
    w = np.ones(m)
    for i in range(1, maxIter + 1):
        z = WhittakerSmooth(x, w, lambda_, porder)
        d = x - z
        dssn = np.abs(d[d < 0].sum())
        if(dssn < 0.001 * (abs(x)).sum() or i == maxIter):
            if(i == maxIter):
                print('airpls: max iteration reached!')
            break
        w[d >= 0] = 0  # d>0 means that this point is part of a peak,
        # so its weight is set to 0 in order to ignore it
        w[d < 0] = np.exp(i * np.abs(d[d < 0]) / dssn)
        w[0] = np.exp(i * (d[d < 0]).max() / dssn)
        w[-1] = w[0]
    return x - z