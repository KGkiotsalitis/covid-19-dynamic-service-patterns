# import solver
import gurobipy as gp #import gurobipy library in Python as gp
from gurobipy import GRB
import pandas as pd #import pandas library as pd. It offers data structures and operations for manipulating numerical tables and time series
import numpy as np #import numpy library. It adds support for large, multi-dimensional arrays and matrices
import os #provides functions for interacting with the operating system
import ast #library that processes trees of the Python abstract syntax grammar

print(gp.gurobi.version())

#Initialize the Gurobi model
model = gp.Model()
model.Params.OutputFlag = 0
model.Params.LogToConsole = 0
#model.setParam("OutputFlag", 0)


S=(1,2,3)
last_stop=3
first_stop=1
u={1:0,2:2,3:0}
h=5 #minutes
p={(1,1):0,(1,2):7,(1,3):8,(2,1):0,(2,2):0,(2,3):19,(3,1):0,(3,2):0,(3,3):0}
g=30
l={(1,1):0,(1,2):0.5,(1,3):0.5,(2,1):0,(2,2):0,(2,3):0.5,(3,1):0,(3,2):0,(3,3):0}
M=1


#Initialize variable x_l denoting the number of vehicles assigned to each line l
x = model.addVars(S,vtype=gp.GRB.BINARY, name='x')
gamma = model.addVars(S,vtype=gp.GRB.CONTINUOUS, name='gamma')
obj_fun = model.addVar(vtype=gp.GRB.CONTINUOUS, name='obj_fun')

model.addConstrs(gamma[y] <= g for y in S)

model.addConstr(gamma[1] == x[1]*sum(p[1,y] for y in S))

model.addConstrs(gamma[s] == gamma[s-1] + x[s]*sum(p[s,y] for y in S if y>s) - sum(p[y,s]*x[y] for y in S if y<=s)
                 for s in S if s!=first_stop if s!=last_stop)

model.addConstr(gamma[last_stop] == 0)

model.addConstr(obj_fun == 0.5*sum(sum((u[s]+(1-x[s]))*h*p[s,y]+h*h*l[s,y] for y in S if y>s) for s in S) )
#Declare objective function
obj = 0.5*sum(sum((u[s]+(1-x[s]))*h*p[s,y]+h*h*l[s,y] for y in S if y>s) for s in S) + M*sum((u[s]+(1-x[s]))*(u[s]+(1-x[s])) for s in S)

#Add objective function to model and declare that we solve a minimization problem
model.setObjective(obj,GRB.MINIMIZE)

model.params.NonConvex = 2 #allow to handle quadratic equality constraints - which are always non-convex
model.optimize()
print('status',GRB.Status.OPTIMAL)
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