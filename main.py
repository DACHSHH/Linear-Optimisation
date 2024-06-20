from data import *
from model import *
import matplotlib.pyplot as plt

############################# solve the model ################################
# Objective: minimize t_max
model.setObjective(t_max, "minimize")

# Solve the model
model.optimize()

# Retrieve and print the results
if model.getStatus() == "optimal":
    print(f"Optimal t_max: {model.getVal(t_max)}")
    for i in I:
        for j in J:
            for w in W:
                print(f"t[{i}][{j}][{w}] = {model.getVal(t[i, j, w])}")
else:
    print("No optimal solution found.")

# Plot the solution
# Initialize the figure and axes
fig, ax = plt.subplots()

############################# Plot the solution ################################

# Plot for each wafer
colors = plt.cm.tab20.colors
handles = []
labels = []
for j in J:
    # if j == 0: # process module 0, comment out if you want to plot other process modules
        for w in W:
            t_values = [model.getVal(t[(i, j, w)]) for i in I]
            ax.step(t_values, range(len(t_values)), color=colors[w % 20], label=f"Wafer {j,w}")
            handles.append(plt.Rectangle((0,0),1,1,color=colors[w % 20]))
            labels.append(f"Wafer {j,w}")

# Set labels and show the plot
ax.set_xlabel("Time")
ax.set_ylabel("Process Step")
# ax.invert_yaxis()
ax.set_aspect('auto')
ax.legend(handles=handles, labels=labels, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()  