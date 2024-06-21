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


