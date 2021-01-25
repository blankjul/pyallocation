from pyallocation.loader import example_problem, load_problem
from pyallocation.solvers.exhaustive import ExhaustiveAlgorithm
from pyallocation.solvers.ilp import ILP, EpsilonConstraintILP
from pyallocation.solvers.ilp import MultiObjectiveILP

# problem = example_problem()
# e = ExhaustiveAlgorithm().setup(problem).solve().opt[0]
# print(f"Example | CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')} ")


for k in range(10):

    problem = load_problem(k)

    res = ILP().setup(problem, verbose=False).solve()
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
