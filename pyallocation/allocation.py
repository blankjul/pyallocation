import numpy as np

from pyallocation.function_loader import FunctionLoader
from pyallocation.util import calc_constr, calc_obj


class FastAllocation:

    def __init__(self, problem, debug=False):
        self.debug = debug
        self.R = problem.R
        self.T = problem.T

        p, n, m = self.T.shape
        self.x = np.full(n, -1)
        self.C = np.full((m, p), 0)
        self.G = np.copy(-self.R)
        self.CV = 0
        self.feas = True
        self.F = np.zeros(p)

    def set(self, j, c):
        T, R, x = self.T, self.R, self.x

        # it has been -1 and we set it to -1. so nothing happens
        if self.x[j] < 0 and c < 0:
            return
        # if both are indeed bigger than one - might be a switch
        elif self.x[j] >= 0 and c >= 0:
            # if the same number we are done
            if self.x[j] == c:
                return
            # otherwise first disable it and then update it later
            else:
                self.set(j, -1)

        _c = x[j]

        x[j] = c

        if c >= 0:
            m = c
            sign = +1
        else:
            m = _c
            sign = -1

        func_loader = FunctionLoader().get_instance()
        calc_cv_1d, calc_consumed = func_loader.load("calc_cv_1d"), func_loader.load("calc_consumed")

        delta = sign * T[:, j, m]
        _cv = calc_cv_1d(self.G[m])

        self.C[m] += delta
        self.G[m] += delta
        self.F += delta

        self.CV += (calc_cv_1d(self.G[m]) - _cv)
        self.feas = self.CV <= 0

        if self.debug:
            _C = calc_consumed(T, x)
            assert np.all(_C == self.C)
            assert np.all(_C - R == self.G)
            assert np.all(self.CV == calc_cv_1d(self.G[m]))
            assert np.all(self.F == calc_obj(self.C))


class Allocation:

    def __init__(self, problem):
        self.R = problem.R
        self.T = problem.T

        p, n, m = self.T.shape
        self.x = np.full(n, -1)
        self.C = np.full((n, m), 0)
        self.G = np.full((n, m), 0)
        self.CV = 0
        self.feas = True
        self.F = np.zeros(p)

    def set(self, i, j):
        self.x[i] = j
        self.update()

    def update(self):
        self.C = FunctionLoader().get_instance().load("calc_consumed")(self.T, self.x)
        self.G = calc_constr(self.C, self.R)
        self.CV = np.maximum(0, self.G).sum()
        self.feas = self.CV <= 0
        self.F = calc_obj(self.C)
