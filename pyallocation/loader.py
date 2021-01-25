import xml.etree.ElementTree as ET

import numpy as np

from pyallocation.problem import AllocationProblem


def example_problem():
    R = np.array([[100, 256, 50],
                  [150, 640, 25],
                  [150, 640, 25],
                  [100, 256, 15]])

    Tcpu = np.array([[10, 90, 90, 55],
                     [50, 20, 20, 72],
                     [30, 20, 20, 72],
                     [10, 40, 40, 72],
                     [20, 40, 40, 72],
                     [20, 50, 50, 55],
                     [90, 20, 20, 15],
                     [20, 10, 10, 70],
                     [20, 10, 10, 70],
                     [20, 15, 15, 70],
                     [90, 10, 10, 33]])

    Tmemory = np.array([[48, 256, 256, 128],
                        [128, 256, 256, 148],
                        [64, 256, 256, 148],
                        [48, 168, 168, 148],
                        [64, 168, 168, 148],
                        [64, 168, 168, 64],
                        [168, 128, 128, 64],
                        [148, 96, 96, 148],
                        [48, 32, 32, 148],
                        [48, 32, 32, 148],
                        [168, 64, 64, 96]])

    Tpower = np.array([[2, 18, 18, 11],
                       [10, 4, 4, 14],
                       [6, 4, 4, 14],
                       [2, 8, 8, 14],
                       [4, 8, 8, 14],
                       [4, 10, 10, 11],
                       [18, 4, 4, 3],
                       [4, 2, 2, 14],
                       [4, 2, 2, 14],
                       [4, 3, 3, 14],
                       [18, 2, 2, 7]])

    T = np.array([Tcpu, Tmemory, Tpower])

    # F = np.array([0.1557, 0.0856, 0.7095, 0.0491])
    w = np.array([0.1557, 0.0856, 0.7095])
    # w = None

    problem = AllocationProblem(R, T, w=w)

    return problem


def load_problem(k):

    root = ET.parse(f'../resources/System{k}.model').getroot()

    avail_attrs = ["cpuAvail", "memAvailable", "powerAvail"]
    constr_attrs = ["cpuCons", "memoryCons", "powerCons"]
    weight_attrs = ["cpuFactor", "memoryFactor", "powerFactor"]

    R = []
    for unit in root.findall("compUnits"):
        R.append([int(float(unit.attrib[a])) for a in avail_attrs])
    R = np.array(R)

    T = []
    for unit in root.findall("resConsumptions"):
        T.append([int(float(unit.attrib[a])) for a in constr_attrs])
    T = np.swapaxes(np.array(T), 0, 1)

    m, p = R.shape
    n = int(T.shape[1] / m)

    T = T.reshape((p, n, m))

    w = np.array([float(root.find("tradeOffvector").attrib[e]) for e in weight_attrs])

    get_constr_component = lambda alloc: int(alloc.attrib["component"].replace("comp", ""))
    get_constr_unit = lambda alloc: int(alloc.attrib["compUnit"].replace("compUnit", ""))

    alloc = []
    for e in root.findall("allocationConstraints"):
        alloc.append((get_constr_component(e), get_constr_unit(e)))

    anti_alloc = []
    for e in root.findall("antiAllocationConstraints"):
        anti_alloc.append((get_constr_component(e), get_constr_unit(e)))

    problem = AllocationProblem(R, T, alloc=alloc, anti_alloc=anti_alloc, w=w)

    return problem
