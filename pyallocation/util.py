import numpy as np


def calc_consumed(T, x):
    p, n, m = T.shape
    C = np.zeros((m, p), dtype=np.int64)
    for j in range(len(x)):
        c = x[j]
        if c >= 0:
            C[c] += T[:, j, c]
    return C


def calc_obj(C, w=None):
    F = C.sum(axis=0)
    if w is not None:
        F = (F * w).sum()
    return F


def calc_constr(C, R):
    return (C - R).flatten()


def is_feasible(C, R):
    return np.all(calc_constr(C, R) <= 0)


def calc_cv_1d(G):
    return np.maximum(0, G).sum()


def calc_cv_2d(G):
    return np.maximum(0, G).sum()
