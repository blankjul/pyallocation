import numpy as np
from pyecore.resources import ResourceSet, URI
from pymoo.util.normalization import normalize
from pymoo.visualization.scatter import Scatter
from pymoo.factory import get_decision_making
from pymoo.configuration import get_pymoo
from pyallocation.problem import AllocationProblem
from pyallocation.util import calc_consumed,calc_obj
import argparse
import sys

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

#Read the input model file
rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI(source_model))
model_root = resource.contents[0]

components = model_root.components
n=len(components)
components_d = {}
for i,c in enumerate(components):
    components_d[c.compName] = i

units = model_root.units
m = len(units)
units_d = {}
for i,u in enumerate(units):
    units_d[u.unitName] = i

resources = model_root.resources
l = len(resources)
resources_d={}
for i,res in enumerate(resources):
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
    alloc.append( (components.index(allocationConstraint.component) , units.index(allocationConstraint.unit) ))

antiAllocationConstraints = model_root.antiAllocationConstraints
anti_alloc = []
for antiAllocationConstraint in antiAllocationConstraints:
    anti_alloc.append( (components.index(antiAllocationConstraint.component) , units.index(antiAllocationConstraint.unit) )) 


def getF(x):
    FL = []
    st =""
    for res in range(len(resources)):
        f_sum = 0;
        for c in range(len(x)):
            f_sum += T[res,c,x[c]]
        FL.append(f_sum)
        st += str(f_sum)+" "

    print(st)
    F = np.array(FL)
    return F

def is_feasible(x):
    m = len(units)
    l = len(resources)
    for u in range(m):
        for res in range(l):
            max_res = R[u,res]
            res_cons = 0
            for c in range(len(x)):
                if x[c]==u:
                    res_cons += T[res,c,x[c]]
            if res_cons > max_res:
                raise ValueError("solution {} is infeasible".format(str(x)))

def check_alloc_and_anti_allo(x):
    for c in range(len(x)):
        u = x[c]
        if (c,u) in anti_alloc:
            raise ValueError("solution {} does not meet an anti-allocation constriant".format(str(x)))
        ind = True
        for comp,un in alloc:
            if comp==c and not(un ==u):
                ind = False
        if not ind:
            raise ValueError("solution {} does not meet an allocation constriant".format(str(x))) 

resource = rset.get_resource(URI('solutionSet.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI(solution_set_model))
model_root = resource.contents[0]
solutions = model_root.solutions
Fs=[]
l_allocs = []
for i,s in enumerate(solutions):
    x=[]
    print("solution "+str(i))
    mappings = s.mappings
    st = ""
    for m in mappings:
        st += m.unitName +" "
        x.append(units_d[m.unitName])
    print(st)
    is_feasible(x)
    check_alloc_and_anti_allo(x)
    F = getF(x)
    Fs.append(F)
    l_allocs.append(i)

if l!= 2 and l!=3:
    print('Number of resources shall be two or three.')
    sys.exit()

labels = [res.resName for res in resources]


dm = get_decision_making("high-tradeoff")
x = np.reshape(Fs, (len(Fs), len(labels)))



plot = Scatter(labels=labels)

d_solutions = {}

for i,f in enumerate(Fs):
        plot.add(f, facecolor="none", edgecolor="red")
        st = f.tobytes()
        if st not in d_solutions.keys():
            d_solutions[st] = 'Solutions '
        d_solutions[st]+=str(l_allocs[i])+','

for s in d_solutions:
    plot.do()
    sol = np.frombuffer(s)
    tu = tuple(sol)
    if len(tu) == 2:
        plot.ax.text(tu[0],tu[1],d_solutions[s])
    elif len(tu) == 3:
        plot.ax.text(tu[0],tu[1],tu[2],d_solutions[s])

try:
    I = dm.do(x)
    print(I)
    plot.add(x[I], color="orange", s=50)
except:
    pass

plot.show()