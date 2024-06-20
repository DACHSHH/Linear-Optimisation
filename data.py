import numpy as np


# Define sets
I = range(10)  # Set of Process Steps, change this number to change the number of process steps
J = range(3)   #  Set of Modules, change this number to change the number of modules
W = range(10)   # Set of Wafers per Module, change this number to change the number of wafers

# Define Sub Sets 
recipe_steps = {1} # Set of process steps where all wafers belonging to a specific run of a module are processed together during a recipe step.
I_recipe = recipe_steps # renamed name for consistency
I_load = set(recipe_step -1 for recipe_step in recipe_steps)
I_unload = set(recipe_step +1 for recipe_step in recipe_steps)

I_automation = {0,2,4}
# T(i,j) is simply the duration of a process step. T is not wafer dependent. This constraint is imposed to simplify the model and means that processing in the automation module is not affected by the order in which wafers are loaded and unloaded from different stations.
# Randomly generate durations between 10 and 100 seconds depending on the process step i and module j
T = {(i, j): np.random.randint(10, 20) for i in I for j in J}
# Set the duration of process step 4 for module 0 to 100 seconds, just for test purposes.
T[1, 0] = 1000
T[1, 2] = 1500
T[1, 3] = 800
# Ramdomly generateted capacipties for all process modules between 5 and 10
C = {j: np.random.randint(5, 10) for j in J}
# set the first capacity to 5, just for test purposes.
C[0] = 5
# Print generated T and C
print("Durations for each step:", T)
print("Capacities for each module:", C)