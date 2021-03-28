import numpy as np
from pyecore.resources import ResourceSet, URI

#Read the input model file named system_n0.model
rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('inputModel_0.model'))
model_root = resource.contents[0]

components = model_root.components
n=len(components)

units = model_root.units
m = len(units)

resources = model_root.resources
l = len(resources)

resource = rset.get_resource(URI('solutionSet.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('solutionSet_0.model'))
model_root = resource.contents[0]

solutions = model_root.solutions
for i,s in enumerate(solutions):
    print("solution "+str(i))
    mappings = s.mappings
    for m in mappings:
        print(m.compName+" "+m.unitName)
