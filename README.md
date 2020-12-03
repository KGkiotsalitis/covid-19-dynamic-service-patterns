# covid-19-dynamic-service-patterns

This repository is meant for publishing the code related to the **deriving dynamic service patterns** in order to comply with the **pandemic-imposed vehicle capacity limits** in public transport operations.

Currently, this repository contains:

1. The `model_case_study.py` script which is the source code of the devised dynamic service pattern model introduced in the paper **A model for modifying the public transport service patterns to account for the imposed COVID-19 capacity**, which is currently under scientific review. This script contains all necessary functions to calculate the solution of the mathematical program for the scenario described in the case study of the scientific paper. 

2. The `hourly_OD_matrix.xlsx` file that contains the average passenger demand during the 1 hour of the study.

# Referencing

In case you use this code for scientific purposes, you can use it by citing the paper **A model for modifying the public transport service patterns to account for the imposed COVID-19 capacity** once it is publicly available.

# License

MIT License

# Dependencies

Note that the script `model_case_study.py` is written in Python. Running or modifying this script requires an installed version of **Python 3.6**. In addition, the mathematical model is solved with the use of **Gurobi 9.0.3**. You would need a Gurobi license to obtain an optimal solution.
