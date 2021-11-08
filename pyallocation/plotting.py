import argparse
import sys

import numpy as np
from pyecore.resources import ResourceSet, URI
from pymoo.factory import get_decision_making
from pymoo.visualization.scatter import Scatter

# Create the parser
my_parser = argparse.ArgumentParser(description='Solve a component allocation problem')

# Add the arguments
my_parser.add_argument('source_model',
                       metavar='source_model',
                       type=str,
                       help='the path to the source model')

my_parser.add_argument('solution_set_model',
                       metavar='solution_set_model',
                       type=str,
                       help='the path to the solution set model')

# Execute the parse_args() method
args = my_parser.parse_args()
source_model = args.source_model
solution_set_model = args.solution_set_model

# Read the input model file
rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI(source_model))
model_root = resource.contents[0]

components = model_root.components
n = len(components)
components_d = {}
for i, c in enumerate(components):
    components_d[c.compName] = i

units = model_root.units
m = len(units)
units_d = {}
for i, u in enumerate(units):
    units_d[u.unitName] = i

resources = model_root.resources
l = len(resources)
resources_d = {}
for i, res in enumerate(resources):
    resources_d[res.resName] = i


def getResourceAvailability(unit, resource):
    resourceAvailabilities = model_root.resourceavailability
    ra = len(resourceAvailabilities)
    for i in range(ra):
        if (resourceAvailabilities[i].resource == resource and resourceAvailabilities[i].unit == unit):
            return resourceAvailabilities[i].amount


R = []
for unit in units:
    r = []
    for i in range(l):
        r.append(float(getResourceAvailability(unit, resources[i])))
    R.append(r)
R = np.array(R)


def getResourceConsumption(unit, resource, component):
    resourceConsumptions = model_root.resourceconsumption
    rc = len(resourceConsumptions)
    for i in range(rc):
        if (resourceConsumptions[i].resource == resource and resourceConsumptions[i].unit == unit and
                resourceConsumptions[i].component == component):
            return resourceConsumptions[i].amount


T = []
for component in components:
    for unit in units:
        res = []
        for resource in resources:
            res.append(float(getResourceConsumption(unit, resource, component)))
        T.append(res)
T = np.swapaxes(np.array(T), 0, 1)
T = T.reshape((l, n, m))

allocationConstraints = model_root.allocationConstraints
alloc = []
for allocationConstraint in allocationConstraints:
    alloc.append((components.index(allocationConstraint.component), units.index(allocationConstraint.unit)))

antiAllocationConstraints = model_root.antiAllocationConstraints
anti_alloc = []
for antiAllocationConstraint in antiAllocationConstraints:
    anti_alloc.append(
        (components.index(antiAllocationConstraint.component), units.index(antiAllocationConstraint.unit)))


def getF(x):
    FL = []
    st = ""
    for res in range(len(resources)):
        f_sum = 0;
        for c in range(len(x)):
            f_sum += T[res, c, x[c]]
        FL.append(f_sum)
        st += str(f_sum) + " "

    print(st)
    F = np.array(FL)
    return F


def is_feasible(x):
    m = len(units)
    l = len(resources)
    for u in range(m):
        for res in range(l):
            max_res = R[u, res]
            res_cons = 0
            for c in range(len(x)):
                if x[c] == u:
                    res_cons += T[res, c, x[c]]
            if res_cons > max_res:
                return False

    return True


def check_alloc_and_anti_allo(x):
    for c in range(len(x)):
        u = x[c]
        if (c, u) in anti_alloc:
            raise ValueError("solution {} does not meet an anti-allocation constriant".format(str(x)))
        ind = True
        for comp, un in alloc:
            if comp == c and not (un == u):
                ind = False
        if not ind:
            raise ValueError("solution {} does not meet an allocation constriant".format(str(x)))


resource = rset.get_resource(URI('solutionSet.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI(solution_set_model))
model_root = resource.contents[0]
solutions = model_root.solutions
l_allocs = []

ID = []
X = []
F = []
feas = []

for i, s in enumerate(solutions):
    x = []
    print("solution " + str(i))
    mappings = s.mappings
    st = ""
    for m in mappings:
        st += m.unitName + " "
        x.append(units_d[m.unitName])
    print(st)
    _feas = is_feasible(x)
    check_alloc_and_anti_allo(x)
    f = getF(x)
    F.append(f)
    l_allocs.append(solutions[i].id)

    feas.append(_feas)
    X.append(x)
    ID.append(int(solutions[i].id))

F = np.array(F)
X = np.array(X)
feas = np.array(feas)

vis_obj_space = False
vis_sols = True

import matplotlib
import matplotlib.pyplot as plt

# matplotlib.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['ps.fonttype'] = 42
# matplotlib.rcParams['text.usetex'] = True

if vis_obj_space:

    plt.figure(figsize=(8, 4))

    plt.scatter(F[feas, 0], F[feas, 1], color="blue", marker="o", label="Feasible")
    plt.scatter(F[~feas, 0], F[~feas, 1], color="red", marker="p", label="Infeasible")

    nds = [4, 5]
    plt.scatter(F[nds, 0], F[nds, 1], color="black", marker="x", s=80, label="Non-Dominated", alpha=0.8)

    for k, f in enumerate(F):
        offset = 0.1
        plt.text(f[0] + offset, f[1] + offset, "$x^{(%s)}$" % (k + 1))

    plt.xlim(16, 23)
    plt.ylim(5, 45)
    plt.xlabel("$f_1$")
    plt.ylabel("$f_2$")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("example.pdf")
    # plt.show()


if vis_sols:

    from pymoo.visualization.petal import Petal

    ideal = F.min(axis=0)
    nadir = F.max(axis=0)

    Petal(bounds=[ideal, nadir], figsize=(3, 4), reverse=True, title="Solution 5").add(F[4]).save(f"petal_sol_5.pdf")
    Petal(bounds=[ideal, nadir], figsize=(3, 4), reverse=True, title="Solution 6").add(F[5]).save(f"petal_sol_6.pdf")
    Petal(bounds=[ideal, nadir], figsize=(3, 4), reverse=True, title="Solution 7").add(F[6]).save(f"petal_sol_7.pdf")

    plt.scatter(F[feas, 0], F[feas, 1], color="blue", marker="o", label="Feasible")
    plt.scatter(F[~feas, 0], F[~feas, 1], color="red", marker="p", label="Infeasible")

    nds = [4, 5]
    plt.scatter(F[nds, 0], F[nds, 1], color="black", marker="x", s=80, label="Non-Dominated", alpha=0.8)

    for k, f in enumerate(F):
        offset = 0.1
        plt.text(f[0] + offset, f[1] + offset, "$x^{(%s)}$" % (k + 1))

    plt.xlim(16, 23)
    plt.ylim(5, 45)
    plt.xlabel("$f_1$")
    plt.ylabel("$f_2$")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("example.pdf")
    # plt.show()


    print("sdfsf")

if l != 2 and l != 3:
    print('Number of resources shall be two or three.')
    sys.exit()

labels = [res.resName for res in resources]

dm = get_decision_making("high-tradeoff")
x = np.reshape(Fs, (len(Fs), len(labels)))

plot = Scatter(labels=labels)

d_solutions = {}

for i, f in enumerate(Fs):
    plot.add(f, facecolor="none", edgecolor="red")
    st = f.tobytes()
    if st not in d_solutions.keys():
        d_solutions[st] = 'Solution '
    d_solutions[st] += str(l_allocs[i])

# try:
#     I = dm.do(x)
#     print(I)
#     plot.add(x[I], color="orange", s=50)
#     plot.do()
# except:
#     pass

plot.show()
