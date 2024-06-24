from pyscipopt import Model
from data import *

# Create the model
model = Model("Scheduling Optimization")

# Define the variables
t = {(i, j, w): model.addVar(vtype="C", name=f"t_{i}_{j}_{w}") for i in I for j in J for w in W}
t_max = model.addVar(vtype="C", name="t_max")

# Add constraints
# (0) t_max should be greater than or equal to all start times
for i in I:
    for j in J:
        for w in W:
            model.addCons(t_max >= t[i, j, w])

# (1) Start times should be non-negative
for i in I:
    for j in J:
        for w in W:
            model.addCons(t[i, j, w] >= 0)

# (2) Sequential order of process steps regarding a unique wafer(j,w)
for i in I:
    for k in I:
        if k > i:
            for j in J:
                for w in W:
                        model.addCons(t[k, j, w] >= t[i, j, w] + T[i, j])

# (3) Sequential order of wafers going through the same process module. No wafer(j,w) of the same process module can overtake a wafer(j,x) of the same process module with x > w.
for i in set(I) - set(I_recipe) : # in in I but not in I_sync_module
    for j in J:
        for w in W:
            for x in W:
                if x > w:#and i != max(I):
                    model.addCons(t[i, j, x] >= t[i, j, w]+ T[i, j])
# (4) Available Space in Process Module before reloading
# A new wafer can only be loaded if wafer of the run before with the same run id which is set by w mod C[j] has been unloaded.
for i in I_load:
    for j in J:
        for w in W:
            for x in W:
                if w % C[j] == x % C[j] and w > x:
                    model.addCons(t[i, j, w] >= t[i+2, j, x] + T[i+2, j])
# (5) Synchronize the start times for wafers processed in the same module when a process module is running
for i in I_recipe:
    for j in J:
        for l in J:
            if j == l:
                for w in W:
                    for x in W:
                        # if the wafer fits into the same run of a process module, then the start time of wafer x in module j is equal to the start time of wafer w in module j.
                        if int(w/C[j]) == int(x/C[j]):
                            model.addCons(t[i, j, x] == t[i, l, w])




#lazy constraints
# benderts decomposition
# Define th large value M