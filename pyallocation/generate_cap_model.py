from pyecore.resources import ResourceSet, URI

rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
root = resource.contents[0]
A = root.getEClassifier('AllocationProblem')
a_instance = A()

components = ['comp1','comp2','comp3','com4','comp5','comp6','comp7','comp8','comp9','comp10','comp11']
n=len(components)
for c in components:
    componentT = root.getEClassifier('Component')
    component_instance = componentT()
    component_instance.compName = c
    a_instance.components.append(component_instance)


units = ['unit1','unit2','unit3','unit4']
m = len(units)
for u in units:
    unitT = root.getEClassifier('Unit')
    unit_instance = unitT()
    unit_instance.unitName = u
    a_instance.units.append(unit_instance)

resources = ['cpu','memory','power']
l = len(resources)
for r in resources:
    resourceT = root.getEClassifier('Resource')
    resource_instance = resourceT()
    resource_instance.resName = r
    a_instance.resources.append(resource_instance)


def generate_TradeOffWeight(F):
    for res in range(l):
        tradeoffweightT = root.getEClassifier('TradeOffWeight')
        tradeOffeight_instance = tradeoffweightT()
        tradeOffeight_instance.weight = F[res]
        tradeOffeight_instance.resource = a_instance.resources[res]
        a_instance.tradeOffvector.append(tradeOffeight_instance)


F = [0.1557, 0.0856, 0.7095]
generate_TradeOffWeight(F)

def generate_Resource_Availabilities(R):
    for u in range(m):
        for r in range(l):
            resourceAvailabilityT = root.getEClassifier('ResourceAvailability')
            resourceAvailability_instance = resourceAvailabilityT()
            resourceAvailability_instance.amount = float(R[u][r])
            resourceAvailability_instance.unit = a_instance.units[u]
            resourceAvailability_instance.resource = a_instance.resources[r]
            a_instance.resourceavailability.append(resourceAvailability_instance)

R = [[100, 256, 50],
	[150, 640, 25],
	[150, 640, 25],
	[100, 256, 15]]
generate_Resource_Availabilities(R)

def generate_Resource_Consumptions(T):
    for res in range(l):
        for comp in range(n):
            for unit in range(m):
                resourceconsumptionT = root.getEClassifier('ResourceConsumption')
                resourceConsumption_instance = resourceconsumptionT()
                resourceConsumption_instance.amount = float(T[res][comp][unit])
                resourceConsumption_instance.component = a_instance.components[comp]
                resourceConsumption_instance.unit = a_instance.units[unit]
                resourceConsumption_instance.resource = a_instance.resources[res]
                a_instance.resourceconsumption.append(resourceConsumption_instance)

T       = [[[10,90,90,55],
        [50,20,20,72],
        [30,20,20,72],
        [10,40,40,72],
        [20,40,40,72],
        [20,50,50,55],
        [90,20,20,15],
        [20,10,10,70],
        [20,10,10,70],
        [20,15,15,70],
        [90,10,10,33]],
            
        [[48,256,256,128],
        [128,256,256,148],
        [64,256,256,148],
        [48,168,168,148],
        [64,168,168,148],
        [64,168,168,64],
        [168,128,128,64],
        [148,96,96,148],
        [48,32,32,148],
        [48,32,32,148],
        [168,64,64,96]],

        [[2,18,18,11],
        [10,4,4,14],
        [6,4,4,14],
        [2,8,8,14],
        [4,8,8,14],
        [4,10,10,11],
        [18,4,4,3],
        [4,2,2,14],
        [4,2,2,14],
        [4,3,3,14],
        [18,2,2,7]]]
generate_Resource_Consumptions(T)


def generate_Allocation_Constraints(alloc):
    for (comp,unit) in alloc:
        allocationconstraintT = root.getEClassifier('AllocationConstraint')
        allocationconstraint_instance = allocationconstraintT()
        allocationconstraint_instance.component = a_instance.components[comp]
        allocationconstraint_instance.unit = a_instance.units[unit]
        a_instance.allocationConstraints.append(allocationconstraint_instance)

alloc = [(6,3)]
generate_Allocation_Constraints(alloc)

def generate_AntiAllocation_Constraints(anti_alloc):
    for (comp,unit) in anti_alloc:
        antiallocationconstraintT = root.getEClassifier('AntiAllocationConstraint')
        antiallocationconstraint_instance = antiallocationconstraintT()
        antiallocationconstraint_instance.component = a_instance.components[comp]
        antiallocationconstraint_instance.unit = a_instance.units[unit]
        a_instance.antiAllocationConstraints.append(antiallocationconstraint_instance)
anti_alloc = [(3,0)]
generate_AntiAllocation_Constraints(anti_alloc)

resource = rset.create_resource(URI('inputModel_0.model'))
resource.append(a_instance)
resource.save()