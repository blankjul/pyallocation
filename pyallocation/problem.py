import numpy as np

from pyallocation.function_loader import FunctionLoader
from pyallocation.util import calc_obj, calc_constr
from pymoo.core.problem import ElementwiseProblem


class AllocationProblem(ElementwiseProblem):

    def __init__(self, R, T, alloc=None, anti_alloc=None, w=None, **kwargs):
        self.R = R
        self.T = T
        self.alloc = alloc
        self.anti_alloc = anti_alloc
        self.w = w
        self.func_calc_consumed = FunctionLoader.get_instance().load("calc_consumed")
        self.ideal = None
        self.nadir = None

        p, n, m = T.shape
        n_var = n

        n_obj = p
        if w is not None:
            n_obj = 1
            assert len(w) == p

        xl = np.full(n_var, 0)
        xu = np.full(n_var, m - 1)
        super().__init__(n_var=n_var, n_obj=n_obj, n_constr=p * m, xl=xl, xu=xu, **kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        R, T, w = self.R, self.T, self.w
        C = self.func_calc_consumed(T, x)
        F = calc_obj(C, w)

        G = list(calc_constr(C, R))

        for pos, val in self.alloc:
            G.append(int(x[pos] != val))

        for pos, val in self.anti_alloc:
            G.append(int(x[pos] == val))

        G = np.array(G)

        out["F"], out["G"] = F.astype(np.float), G.astype(np.float)
