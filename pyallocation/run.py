import pickle

from pyallocation.loader import load_problem
from pyallocation.solvers.ilp import MultiObjectiveILP
from pymoo.util.normalization import normalize
from pymoo.visualization.pcp import PCP
from pymoo.visualization.scatter import Scatter

# problem = example_problem()
# e = ExhaustiveAlgorithm().setup(problem).solve().opt[0]
# print(f"Example | CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')} ")


# for k in range(8):
k = 8
problem = load_problem(k)

res = MultiObjectiveILP().setup(problem, verbose=False).run()
pickle.dump(res, open("solutions.dat", "wb"))

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
