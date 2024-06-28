from data import *
from model import *
import csv

############################# solve the model ################################
# Objective: minimize t_max
model.setObjective(t_max, "minimize")

# Set the relative gap tolerance. Means the gap to the optimum
model.setRealParam('limits/gap', 0.2)  # 0.1 corresponds to 10%
# Solve the model
model.optimize()

# Retrieve and print the results
if model.getStatus() in ["optimal", "gaplimit", "bestsollimit"]:
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
    for i in I_automation:
        for j in J:
            for w in W:
                for k in I_automation:
                    for l in J:
                        for x in W:               
                            if (i,j,w) > (k,l,x) and model.getVal(t[k, l, x]) >= model.getVal(t[i, j, w]) and model.getVal(t[k, l, x]) < model.getVal(t[i, j, w]) + T[i,j]:
                                print(f"Overlapping in automation between t{i,j,w} and t{k,l,x}. You might need to increase M")
                                test = False
    if test:
        print(f"Optimal t_max: {model.getVal(t_max)}")
else:
    print("No optimal solution found.")


