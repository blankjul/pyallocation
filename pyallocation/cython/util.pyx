# distutils: language = c++
# cython: language_level=2, boundscheck=False, wraparound=False, cdivision=True

import numpy as np

def calc_consumed(T, x):
    p, _, m = T.shape
    C = np.zeros((m, p), dtype=np.int64)
    c_calc_consumed_impl(T, x, C)
    return C



cdef c_calc_consumed_impl(long[:,:,:] T, long[:] x, long[:,:] C):
    cdef int i, j, c
    for i in range(len(T)):
        for j in range(len(x)):
            c = x[j]
            if c >= 0:
                C[c][i] += T[i][j][c]



def calc_cv_1d(long[:] G):
    return c_calc_cv_1d(G)

cdef c_calc_cv_1d(long[:] G):
    cdef int i, max_i, v
    max_i = len(G)
    v = 0
    for i in range(max_i):
        g = G[i]
        if g > 0:
            v += g
    return v


def calc_cv_2d(long[:,:] G):
    return c_calc_cv_2d(G)

cdef c_calc_cv_2d(long[:,:] G):
    cdef int i, j, max_i, max_j, v
    max_i = G.shape[0]
    max_j = G.shape[1]
    v = 0

    for i in range(max_i):
        for j in range(max_j):
            g = G[i][j]
            if g > 0:
                v += g
    return v










