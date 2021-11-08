from pyecore.resources import ResourceSet, URI

rset = ResourceSet()
resource = rset.get_resource(URI('componentAllocation2.ecore'))
root = resource.contents[0]
A = root.getEClassifier('AllocationProblem')
a_instance = A()

components = ['comp1','comp2']
n=len(components)
for c in components:
    componentT = root.getEClassifier('Component')
    component_instance = componentT()
    component_instance.compName = c
    a_instance.components.append(component_instance)


units = ['unit1','unit2']
m = len(units)
for u in units:
    unitT = root.getEClassifier('Unit')
    unit_instance = unitT()
    unit_instance.unitName = u
    a_instance.units.append(unit_instance)

resources = ['res1','res2',]
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


F = [0.75, 0.25]
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

R = [[14,22],
	[20,40]]
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

T       = [
        [[10,7],
        [5,12]],
            
        [[15,20],
        [5,17]]
        ]
generate_Resource_Consumptions(T)


def generate_Allocation_Constraints(alloc):
    for (comp,unit) in alloc:
        allocationconstraintT = root.getEClassifier('AllocationConstraint')
        allocationconstraint_instance = allocationconstraintT()
        allocationconstraint_instance.component = a_instance.components[comp]
        allocationconstraint_instance.unit = a_instance.units[unit]
        a_instance.allocationConstraints.append(allocationconstraint_instance)

alloc = []
generate_Allocation_Constraints(alloc)

def generate_AntiAllocation_Constraints(anti_alloc):
    for (comp,unit) in anti_alloc:
        antiallocationconstraintT = root.getEClassifier('AntiAllocationConstraint')
        antiallocationconstraint_instance = antiallocationconstraintT()
        antiallocationconstraint_instance.component = a_instance.components[comp]
        antiallocationconstraint_instance.unit = a_instance.units[unit]
        a_instance.antiAllocationConstraints.append(antiallocationconstraint_instance)
anti_alloc = []
generate_AntiAllocation_Constraints(anti_alloc)

resource = rset.create_resource(URI('../resources/inputModel_demo.model'))
resource.append(a_instance)
resource.save()