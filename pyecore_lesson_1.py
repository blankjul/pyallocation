from pyecore.ecore import EClass, EAttribute, EString, EObject, EReference
from pyecore.resources import ResourceSet, URI
import numpy as np
from pyallocation.solvers.exhaustive import ExhaustiveAlgorithm
from pyallocation.solvers.ilp import ILP, EpsilonConstraintILP
from pyallocation.solvers.ilp import MultiObjectiveILP
from pyallocation.problem import AllocationProblem

rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('System0.model'))
model_root = resource.contents[0]
#print(model_root.components[0].resConsumptions[0].cpuCons)

components = model_root.components
# count = 0 
# for c in components:
#     count +=1
# n= count
# print(n)

units = model_root.compUnits
# count = 0 
# for c in units:
#     count +=1
# m= count
# print(m)

tradeOffvector = model_root.tradeOffvector
F = []
F.append(tradeOffvector.cpuFactor)
F.append(tradeOffvector.memoryFactor)
F.append(tradeOffvector.powerFactor)
w = np.array(F)
print(w)

R = []
for unit in units:
    r = [int(float(unit.cpuAvail))]
    r.append(int(float(unit.memAvailable)))
    r.append(int(float(unit.powerAvail)))
    R.append(r)
R = np.array(R)
print(R)

resConsumptions = model_root.resConsumptions
T = []
for resConsumption in resConsumptions:
    res = [int(float(resConsumption.cpuCons))]
    res.append(int(float(resConsumption.memoryCons)))
    res.append(int(float(resConsumption.powerCons)))
    T.append(res)
print(T)
T = np.swapaxes(np.array(T), 0, 1)
print(T)
m, p = R.shape
n = int(T.shape[1] / m)
T = T.reshape((p, n, m))

get_constr_component = lambda alloc: int(alloc.component.compName.replace("comp", ""))
get_constr_unit = lambda alloc: int(alloc.compUnit.compUnitName.replace("compUnit", ""))

allocationConstraints = model_root.allocationConstraints
alloc = []
for allocationConstraint in allocationConstraints:
    alloc.append( (get_constr_component(allocationConstraint ) , get_constr_unit(allocationConstraint )))
print(alloc)  

antiAllocationConstraints = model_root.antiAllocationConstraints
anti_alloc = []
for antiAllocationConstraint in antiAllocationConstraints:
    anti_alloc.append( (get_constr_component(antiAllocationConstraint ) , get_constr_unit(antiAllocationConstraint )))
print(anti_alloc)  

problem = AllocationProblem(R, T, alloc=alloc, anti_alloc=anti_alloc, w=w)
res = ILP().setup(problem, verbose=False).solve()
for e in res.pop:
        print(f"System 0 | CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')} ")