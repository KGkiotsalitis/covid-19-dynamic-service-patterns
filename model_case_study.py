# Author Details:
# Dr Konstantinos Gkiotsalitis
# Assistant Professor
# University of Twente
# Contact: k.gkiotsalitis@utwente.nl
#
# License:
# MIT License
#
# Required libraries:
# numpy, os, pandas, gurobipy
#
# Programming language:
# Python 3
#
# Optimization solver:
# Gurobi 9

# Import libraries
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import os
import ast

# Check version of your Gurobi installation
print(gp.gurobi.version())

# Initialize the Gurobi model
model = gp.Model()
model.Params.OutputFlag = 0
model.Params.LogToConsole = 0

# Introduce the input data from the case study
S=(1,2,3,4,5,6,7,8,9,10,11,12,13)
last_stop=13
first_stop=1
df=pd.read_excel (r'hourly_OD_matrix.xlsx')
print (df)

p={(i,j):df.at[i-1,j] for i in S for j in S}
print(p)

u={1:0,2:0,3:0,4:0,5:0,6:2,7:1,8:1,9:0,10:1,11:0,12:1,13:0}
h=5 #minutes
g=59 #59 pandemic-imposed, 81 nominal
for i in S:
    for j in S:
        p[i,j]=p[i,j]*0.083333*(u[i]+1)
l={(i,j):0 for i in S for j in S}
M=10000


# Initialize the variables of the model
x = model.addVars(S,vtype=gp.GRB.BINARY, name='x')
gamma = model.addVars(S,vtype=gp.GRB.CONTINUOUS, name='gamma')
obj_fun = model.addVar(vtype=gp.GRB.CONTINUOUS, name='obj_fun')

# Add the problem constraints
model.addConstrs(gamma[y] <= g for y in S)

model.addConstr(gamma[1] == x[1]*sum(p[1,y] for y in S))

model.addConstrs(gamma[s] == gamma[s-1] + x[s]*sum(p[s,y] for y in S if y>s) - sum(p[y,s]*x[y] for y in S if y<=s)
                 for s in S if s!=first_stop if s!=last_stop)

model.addConstr(gamma[last_stop] == 0)

model.addConstr(obj_fun == 0.5*sum(sum((u[s]+(1-x[s]))*h*p[s,y]+h*h*l[s,y] for y in S if y>s) for s in S) )

# Declare the objective function
obj = 0.5*sum(sum((u[s]+(1-x[s]))*h*p[s,y]+h*h*l[s,y] for y in S if y>s) for s in S) + M*sum((u[s]+(1-x[s]))*(u[s]+(1-x[s])) for s in S)

# Solve the minimization problem
model.setObjective(obj,GRB.MINIMIZE)

model.params.NonConvex = 2 #allow to handle quadratic equality constraints - which are always non-convex
model.optimize()
print('status',GRB.Status.OPTIMAL)

# Return solution
print(model.printQuality())
for v in model.getVars():
    print('%s %g' % (v.varName, v.x))

variable=[]
solution=[]
for v in model.getVars():
    variable.append(v.varName)
    solution.append(v.x)
print("variable name",variable)
print("solution",solution)