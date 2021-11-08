import contextlib
import io
from copy import copy

import numpy as np
from ortools.linear_solver import pywraplp

from pymoo.core.evaluator import Evaluator
from pymoo.factory import get_reference_directions
from pymoo.core.algorithm import Algorithm
from pymoo.core.individual import Individual
from pymoo.core.population import Population
from pymoo.util.termination.no_termination import NoTermination

from pyallocation.problem import AllocationProblem


def define(T, R, w, alloc=None, anti_alloc=None, ideal=None, nadir=None):
    p, n, m = T.shape

    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = []
    for i in range(n):
        x.append([solver.IntVar(0, 1, f'x[{i + 1},{j + 1}]') for j in range(m)])
    x = np.array(x)

    # each row should sum up to one
    for row in x:
        solver.Add(sum(row) == 1)

    # for each factor
    for i in range(p):

        # add the constraints for each assignment
        for j in range(m):
            solver.Add(sum([T[i][k][j] * x[k][j] for k in range(n)]) <= R[j][i])

    # make sure the allocation constraint is satisfied
    for i, j in alloc:
        solver.Add(x[i][j] == 1)

    # make sure the allocation constraint is satisfied
    for i, j in anti_alloc:
        solver.Add(x[i][j] == 0)

    F = (T * x).sum(axis=1).sum(axis=1)

    if ideal is not None:
        F = F - ideal

        if nadir is not None:
            F = F / (nadir - ideal)

    f = F @ w

    solver.Minimize(f)

    return solver, x


def solve(solver, x, verbose=False):
    status = solver.Solve()

    if status not in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        return None

    if verbose:

        if status == pywraplp.Solver.OPTIMAL:
            print('Solution:')
            print('Objective value =', solver.Objective().Value())
            for r in x:
                for e in r:
                    print(int(e.solution_value()), end=" ")
                print()

        else:
            print('The problem does not have an optimal solution.')

        print('\nAdvanced usage:')
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
        print()

    opt = []
    for _x in x:
        v = np.where(np.array([e.solution_value() for e in _x]))[0][0]
        opt.append(v)
    opt = np.array(opt)

    return opt


class ILP(Algorithm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_termination = NoTermination()

    def _setup(self, problem, **kwargs):
        assert isinstance(problem, AllocationProblem)

    def _initialize_advance(self, **kwargs):
        problem = self.problem
        T, R, alloc, anti_alloc, w = problem.T, problem.R, problem.alloc, problem.anti_alloc, problem.w
        ideal, nadir = problem.ideal, problem.nadir

        opt = solve(*define(T, R, w, alloc=alloc, anti_alloc=anti_alloc, ideal=ideal, nadir=nadir), verbose=self.verbose)

        pop = Population.create(Individual(X=opt, w=w))
        self.evaluator.eval(problem, pop)
        self.pop = pop
        self.termination.force_termination = True


class MultiObjectiveILP(ILP):

    def __init__(self, W=None, **kwargs):
        super().__init__(**kwargs)
        self.default_termination = NoTermination()
        self.W = W

    def _setup(self, problem, **kwargs):
        assert isinstance(problem, AllocationProblem)

    def _initialize_advance(self, **kwargs):
        pop = Population()

        problem = copy(self.problem)


        extremes =  Population()

        W = np.eye(3)
        W[W == 0] = 1e12

        for w in W:
            problem.w = w
            ret = ILP().setup(problem).run().pop
            extremes = Population.merge(extremes, ret)

        problem.w = None
        Evaluator().eval(problem, extremes, skip_already_evaluated=False)

        F = extremes.get("F")
        ideal, nadir = F.min(axis=0), F.max(axis=0)

        problem.ideal = ideal
        problem.nadir = nadir

        W = self.W
        if W is None:
            W = get_reference_directions("das-dennis", 3, n_partitions=12)

        for w in W:
            problem.w = w
            res = ILP().setup(problem).run()
            pop = Population.merge(pop, res.opt)
            problem.w = None
            F = problem.evaluate(pop.get("X"), return_values_of=["F"])
            pop.set("F", F)

        self.pop = pop
        self.termination.force_termination = True


class EpsilonConstraintILP(ILP):

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
        problem = copy(self.problem)
        problem.w = None

        T, R, alloc, anti_alloc = problem.T, problem.R, problem.alloc, problem.anti_alloc

        extreme = MultiObjectiveILP(np.eye(3)).setup(self.problem).solve().pop
        self.pop = Population.merge(self.pop, extreme)
        F = extreme.get("F")
        ideal, nadir = F.min(axis=0), F.max(axis=0)

        for i in range(3):

            W = get_reference_directions("das-dennis", 2, n_points=30 + 2)[1:-1]

            for w in W:
                solver, x = define(T, R, np.ones(3), alloc=alloc, anti_alloc=anti_alloc)

                def obj(k):
                    return (T[k] * x[:, [k]]).sum()

                for j, o in enumerate([e for e in range(3) if e != i]):
                    eps = ideal[o] + w[j] * (nadir[o] - ideal[o])
                    solver.Add(obj(o) <= eps)

                solver.Minimize(obj(i))
                opt = solve(solver, x, verbose=False)
                if opt is not None:
                    pop = Population.create(Individual(X=opt, w=w))
                    self.evaluator.eval(problem, pop)
                    self.pop = Population.merge(self.pop, pop)



        self.termination.force_termination = True
