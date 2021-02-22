import numpy as np
from pyecore.resources import ResourceSet, URI

from pyallocation.problem import AllocationProblem
from pyallocation.solvers.ilp import ILP

rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('system_n0.model'))
model_root = resource.contents[0]
# print(model_root.components[0].compName)

components = model_root.components
n = len(components)
# print(n)

units = model_root.units
m = len(units)
# print(m)

resources = model_root.resources
l = len(resources)
# print(l)

F = []
for i in range(l):
    F.append(model_root.tradeOffvector[i].weight)
w = np.array(F)


# w = print(w)

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
        r.append(int(float(getResourceAvailability(unit, resources[i]))))
    R.append(r)
R = np.array(R)


# print(R)

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
            res.append(int(float(getResourceConsumption(unit, resource, component))))
        T.append(res)
# print(T)
T = np.swapaxes(np.array(T), 0, 1)
# print(T)
T = T.reshape((l, n, m))

allocationConstraints = model_root.allocationConstraints
alloc = []
for allocationConstraint in allocationConstraints:
    alloc.append((components.index(allocationConstraint.component), units.index(allocationConstraint.unit)))
# print(alloc)

antiAllocationConstraints = model_root.antiAllocationConstraints
anti_alloc = []
for antiAllocationConstraint in antiAllocationConstraints:
    anti_alloc.append(
        (components.index(antiAllocationConstraint.component), units.index(antiAllocationConstraint.unit)))
# print(anti_alloc)

problem = AllocationProblem(R, T, alloc=alloc, anti_alloc=anti_alloc, w=w)
res = ILP().setup(problem, verbose=False).solve()
for e in res.pop:
    print(f"System n0 | CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')} ")
