import numpy as np
from pymoo.model.algorithm import Algorithm
from pymoo.model.population import Population
from pymoo.util.termination.no_termination import NoTermination

from pyallocation.allocation import FastAllocation
from pyallocation.problem import AllocationProblem


def exhaustively(problem):
    alloc = FastAllocation(problem, debug=False)
    k = 0
    sols = []
    rec_exhaustively(problem, alloc, k, sols)
    sols.sort(key=lambda x: (x[1], x[2]))
    return sols[:100]


def rec_exhaustively(problem, alloc, k, sols):
    if not alloc.feas:
        return

    if k == problem.n_var:
        x, cv, f = np.copy(alloc.x), alloc.CV, (alloc.F * problem.w).sum()
        sols.append((x, cv, f))

        if len(sols) > 1000:
            sols.sort(key=lambda x: (x[1], x[2]))
            while len(sols) > 100:
                sols.pop()

    else:
        for val in range(problem.xl[k], problem.xu[k] + 1):
            alloc.set(k, val)
            rec_exhaustively(problem, alloc, k + 1, sols)
            alloc.set(k, -1)



class ExhaustiveAlgorithm(Algorithm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_termination = NoTermination()

    def setup(self, problem, **kwargs):
        super().setup(problem, **kwargs)
        assert isinstance(problem, AllocationProblem)
        return self

    def _initialize(self):
        self._next()

    def _next(self):
        solutions = exhaustively(self.problem)

        self.pop = Population.new(X=np.array([x for x, _, _ in solutions]))
        self.evaluator.eval(self.problem, self.pop)

        for ind in self.pop:
            print(ind.F[0], ind.X)

        self.termination.force_termination = True
