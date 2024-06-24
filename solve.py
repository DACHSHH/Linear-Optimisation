from data import *
from model import *
import csv

############################# solve the model ################################
# Objective: minimize t_max
model.setObjective(t_max, "minimize")

# Solve the model
model.optimize()

# Retrieve and print the results
if model.getStatus() == "optimal":
    with open('t(i,j,w)_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i in I:
            for j in J:
                for w in W:
                    print(f"t[{i}][{j}][{w}] = {model.getVal(t[i, j, w])}")
                    # Write results
                    writer.writerow({model.getVal(t[i, j, w])})
        writer.writerow({model.getVal(t_max)})
    test = True
    for i in I:
        for j in J:
            for w in W:
                for k in I:
                    for l in J:
                        for x in W:               
                            if i in I_automation and (i,j,w) > (k,l,x) and model.getVal(t[k, l, x]) >= model.getVal(t[i, j, w]) and model.getVal(t[k, l, x]) < model.getVal(t[i, j, w]) + T[i,j]:
                                print(f"Overlapping in automation between t{i,j,w} and t{k,l,x}. You might need to increase M")
                                test = False
    if test:
        print(f"Optimal t_max: {model.getVal(t_max)}")
else:
    print("No optimal solution found.")


