from data import *
from model import *
import csv

############################# solve the model ################################
# Objective: minimize t_max
model.setObjective(t_max, "minimize")

model.optimize()

M = 10000  # this should be larger than any maximum difference expected between start times
y = {}
for i in I:
    for j in J:
        for w in W:
            for k in I:
                for l in J:
                    for x in W:
                        if model.getVal(t[k, l, x]) - model.getVal(t[i, j, w]) >= 0 and model.getVal(t[k, l, x]) - model.getVal(t[i, j, w]) >= T[i, j]:
                            pass
                        elif model.getVal(t[i, j, w]) - model.getVal(t[k, l, x]) < 0 and  model.getVal(t[i, j, w]) - model.getVal(t[k, l, x]) >= T[k, l]:
                            pass
                        elif (k, l, x) < (i, j, w) and not (l == j and x == w) and not (k == i and l == j): # avoids comparing the same process steps twice and avoids comparing two steps of the same wafer (j,w) because (2) already holds and avoids comparing the same process module in its same process step because (3) holds.
                            model.setObjective(t_max, "minimize")
                            y[(k, l, x, i, j, w)] = model.addVar(vtype="B", name=f"y_{k}_{l}_{x}_{i}_{j}_{w}")
                            model.addCons(t[k, l, x] - t[i, j, w] + M * y[k, l, x, i, j, w] >= T[i, j])
                            model.addCons(t[i, j, w] - t[k, l, x] + M * (1 - y[k, l, x, i, j, w]) >= T[k, l])
                            # Solve the model
                            model.optimize()


# Retrieve and print the results
if model.getStatus() == "optimal":
    print(f"Optimal t_max: {model.getVal(t_max)}")
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in I:
            for j in J:
                for w in W:
                    print(f"t[{i}][{j}][{w}] = {model.getVal(t[i, j, w])}")
                    # Write results
                    writer.writerow({model.getVal(t[i, j, w])})
else:
    print("No optimal solution found.")


