

================
pyallocation
================


----------
Validation
----------
The OCL-based program for validating CAP modes is provided in *CAP Models Validation.zip*.

To validate a CAP model, *e.g.,* system_n0.model, enter the following from within the CAP Models Validation directory:

**java -jar ./ExecutableOne.jar system_n0.model**

----------
Transformation
----------


----------
Solver
----------
The main Python scripts are:

1. solve\_cap\_single\_objective.py

This one solves single-objective component allocation problems.

**Usage:** python .\\solve\_cap\_single\_objective.py ..\\resources\\system\_n1.model ..\\resources\\solutionSet\_1.model

2. solve\_cap\_multi\_objective.py

This one solves multi-objective component allocation problems.

**Usage:** python .\\solve\_cap\_multi\_objective.py ..\\resources\\system\_n1.model ..\\resources\\solutionSet\_1\_mo.model

3. visualize\_solution\_set.py

This one plots the solution set on a 3D scatter plot. In the plot, the high trade-off point(s) are shown in orange.

**Usage:** python .\\visualize\_solution\_set.py ..\\resources\\system\_n1.model ..\\resources\\solutionSet\_1\_mo.model

4. visualize\_a\_single\_solution.py

This one visualizes a single solution using a Petal Diagram.

**Usage:** python .\\visualize\_a\_single\_solution.py ..\\resources\\system\_n1.model ..\\resources\\solutionSet\_1\_mo.model 10

5. visualize\_solution\_set\_Pseudo\_Weights.py

This one visualizes the solution obtained using the pseudo-weight vector approach.

**Usage:** python .\\visualize\_solution\_set\_Pseudo\_Weights.py ..\\resources\\system\_n1.model ..\\resources\\solutionSet\_1\_mo.model

----------
Postprocessing
----------


.. _Contact:

----------
Contact
----------

Feel free to contact me if you have any question:

| `Issam Al-Azzoni <https://engineering.aau.ac.ae/en/academic-staff/staff/issam-al-azzoni>`_  (issam.alazzoni [at] aau.ac.ae)
| Al Ain University
| College of Engineering
| Abu Dhabi - United Arab Emirates
|
| `Julian Blank <http://julianblank.com>`_  (blankjul [at] egr.msu.edu)
| Michigan State University
| Computational Optimization and Innovation Laboratory (COIN)
| East Lansing, MI 48824, USA



