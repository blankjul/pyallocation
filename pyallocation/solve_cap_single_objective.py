import numpy as np
import argparse
from pyecore.resources import ResourceSet, URI
from pyallocation.problem import AllocationProblem
from pyallocation.solvers.ilp import ILP

# Create the parser
my_parser = argparse.ArgumentParser(description='Solve a component allocation problem')

# Add the arguments
my_parser.add_argument('source_model',
                       metavar='source_model',
                       type=str,
                       help='the path to the source model')

my_parser.add_argument('target_model',
                       metavar='target_model',
                       type=str,
                       help='the path to the target model')

# Execute the parse_args() method
args = my_parser.parse_args()
source_model = args.source_model
target_model = args.target_model

#Read the input model file
rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI(source_model))
model_root = resource.contents[0]

components = model_root.components
n=len(components)

units = model_root.units
m = len(units)

resources = model_root.resources
l = len(resources)

F = []
for i in range(l):
    F.append(model_root.tradeOffvector[i].weight)
w = np.array(F)

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
    alloc.append( (components.index(allocationConstraint.component) , units.index(allocationConstraint.unit) ))

antiAllocationConstraints = model_root.antiAllocationConstraints
anti_alloc = []
for antiAllocationConstraint in antiAllocationConstraints:
    anti_alloc.append( (components.index(antiAllocationConstraint.component) , units.index(antiAllocationConstraint.unit) )) 

#Solve the component allocation problem
problem = AllocationProblem(R, T, alloc=alloc, anti_alloc=anti_alloc, w=w)
res = ILP().setup(problem, verbose=False).solve()

for e in res.pop:
        print("System {}".format(model_root.ID))
        print(f"CV = {e.CV[0]} | F = {e.F} | X = {e.X} | w={e.get('w')}")

#Output the solution set
resource = rset.get_resource(URI('solutionSet.ecore'))
root = resource.contents[0]
A = root.getEClassifier('SolutionSet')
a_instance = A()

for e in res.pop:
    sT = root.getEClassifier('Solution')
    s_instance = sT()
    a_instance.solutions.append(s_instance)

    solution = e.X
    for i, j in enumerate(solution):
        mappingT = root.getEClassifier('Mapping')
        mapping_instance = mappingT()
        mapping_instance.compName = components[i].compName
        mapping_instance.unitName = units[j].unitName
        s_instance.mappings.append(mapping_instance)

rset = ResourceSet()
resource = rset.create_resource(URI(target_model))
resource.append(a_instance)
resource.save()
