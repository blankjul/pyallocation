

================
pyallocation
================


----------
Validation
----------



The program *solve\_cap\_in\_a\_model\_file.py* reads the input model file *system\_n0.model*,
solves the component allocation problem, and stores the optimal solution set in the output model file *solutionSet\_0.model*.
The input meta-model file is *componentAllocation2.ecore* and the output meta-model file is *solutionSet.ecore*.
This version of the program assumes a variable number of resources (i.e., the updated meta-model for the component allocation problem is used).

----------
Transformation
----------


----------
Solver
----------
The main Python scripts are:

1. solve\_cap\_single\_objective.py

This one solves single-objective component allocation problems.

Usage: python .\solve\_cap\_single\_objective.py ..\resources\system\_n1.model ..\resources\solutionSet\_1.model

1. solve\_cap\_multi\_objective.py

This one solves multi-objective component allocation problems.

Usage: python .\solve\_cap\_multi\_objective.py ..\resources\system\_n1.model ..\resources\solutionSet\_1\_mo.model

1. visualize\_solution\_set.py

This one plots the solution set on a 3D scatter plot. In the plot, the high trade-off point(s) are shown in orange.

Usage: python .\visualize\_solution\_set.py ..\resources\system\_n1.model ..\resources\solutionSet\_1\_mo.model

**TO DO:** We need to label each solution point in the objective space with the corresponding solution id.

1. visualize\_a\_single\_solution.py

This one visualizes a single solution using a Petal Diagram.

Usage: python .\visualize\_a\_single\_solution.py ..\resources\system\_n1.model ..\resources\solutionSet\_1\_mo.model 10

1. visualize\_solution\_set\_Pseudo\_Weights.py

This one visualizes the solution obtained using the pseudo-weight vector approach.

Usage: python .\visualize\_solution\_set\_Pseudo\_Weights.py ..\resources\system\_n1.model ..\resources\solutionSet\_1\_mo.model

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



