import pickle

import numpy as np

from pyallocation.loader import load_problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.crossover import Crossover
from pymoo.core.duplicate import DefaultDuplicateElimination
from pymoo.core.mutation import Mutation
from pymoo.core.repair import Repair
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.util.normalization import normalize
from pymoo.visualization.pcp import PCP
from pymoo.visualization.scatter import Scatter

# problem = example_problem()
# e = ExhaustiveAlgorithm().setup(problem).solve().opt[0]
# print(f"Example | CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')} ")


for k in range(10):
    # k = 3
    problem = load_problem(k)
    problem.w = None


    class MyCrossover(Crossover):
        def __init__(self):
            super().__init__(2, 1)

        def _do(self, problem, X, **kwargs):
            n_parents, n_matings, n_var = X.shape

            _X = np.full((self.n_offsprings, n_matings, problem.n_var), -1)

            for k in range(n_matings):

                for i in range(n_var):

                    if np.random.random() < 0.5:
                        p = 0
                    else:
                        p = 1

                    _X[0, k, i] = X[p, k, i]

            return _X


    class MyMutation(Mutation):
        def _do(self, problem, X, **kwargs):
            n, m = X.shape

            for i in range(n):

                for j in range(m):

                    if np.random.random() < 0.05:
                        X[i, j] = np.random.choice(np.arange(problem.xl[j], problem.xu[j] + 1).astype(int))

            return X


    class MyRepair(Repair):

        def _do(self, problem, pop, **kwargs):

            # the packing plan for the whole population (each row one individual)
            Z = pop.get("X")

            # now repair each individual i
            for i in range(len(Z)):

                for (pos, val) in problem.alloc:
                    Z[i, pos] = val

                for (pos, val) in problem.anti_alloc:
                    if Z[i, pos] == val:
                        cands = [e for e in range(int(problem.xl[pos]), int(problem.xu[pos] + 1)) if e != val]
                        Z[i, pos] = np.random.choice(cands)

            pop.set("X", Z)
            return pop


    method = NSGA2(pop_size=100,
                   sampling=get_sampling("int_random"),
                   crossover=MyCrossover(),
                   mutation=MyMutation(),
                   repair=MyRepair(),
                   eliminate_duplicates=True,
                   )

    res = minimize(problem,
                   method,
                   termination=('n_gen', 100),
                   seed=1,
                   verbose=False,
                   save_history=True
                   )

    opt = DefaultDuplicateElimination(func=lambda pop: pop.get("F")).do(res.opt)

    # res = MultiObjectiveILP().setup(problem, verbose=False).run()
    # pickle.dump(res, open("solutions.dat", "wb"))
    #
    # opt = DefaultDuplicateElimination().do(res.pop)

    print(f"System {k}: {len(opt)} solutions.")

res = pickle.load(open("solutions.dat", "rb"))

F = res.F
F_norm = normalize(F)
ideal = F.min(axis=0)
nadir = F.max(axis=0)

labels = ["CPU", "Memory", "Power"]

# Scatter(labels=labels).add(F, facecolor="none", edgecolor="red").show()

s = 15

plot = Scatter(labels=labels[:3])
plot.add(F[:, :3], color="grey", alpha=0.3)
plot.add(F[s, :3], color="red")
plot.show()

# plot.ax.text(x, y, z, '%s' % (label), size=20, zorder=1, color='k')
# plot.ax.text(F[s, 0], F[s, 1], F[s, 2], "selected")

# import matplotlib
# matplotlib.pyplot.show()


plot = PCP(labels=labels, legend=True)
plot.set_axis_style(color="grey", alpha=0.5)
plot.add(F, color="grey", alpha=0.3)
plot.add(F[s], linewidth=5, color="red", label="Solution X")
plot.show()

#
# plot = Petal(bounds=(0, 1), reverse=False, labels=labels, title="Solution X")
# plot.add(F_norm[s])
# plot.show()

# plot = Radar(bounds=(0, 1), normalize_each_objective=False)
# plot.add(F_norm[s])
# plot.show()

# print(f"----------------------------")
# print(f"System{k}")
# print(f"----------------------------")
for e in res.pop:
    print(f"System{k} | CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')} ")

#
#
# if w is None:
#
#     ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)
#
#     method = NSGA3(ref_dirs,
#                    pop_size=200,
#                    sampling=get_sampling("int_lhs"),
#                    crossover=get_crossover("int_sbx", prob=1.0, eta=10.0),
#                    mutation=get_mutation("int_pm", eta=10.0),
#                    eliminate_duplicates=True,
#                    )
#
#     res = minimize(problem,
#                    method,
#                    seed=1,
#                    save_history=True,
#                    verbose=True
#                    )
#
#     Scatter().add(res.F).show()
#
#     for ind in res.opt:
#         print(ind.w, ind.X)
#
# else:
#
#     method = GA(
#         pop_size=100,
#         sampling=get_sampling("int_random"),
#         crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
#         mutation=get_mutation("int_pm", eta=3.0),
#         eliminate_duplicates=True,
#     )
#
#     res = minimize(problem,
#                    method,
#                    seed=1,
#                    save_history=True
#                    )
#
#     print("Best solution found: %s" % res.X)
#     print("Function value: %s" % res.F)
#     print("Constraint violation: %s" % res.CV)
