import numpy as np
import csv

# Define sets
I = range(3)  # Set of Process Steps, change this number to change the number of process steps
J = range(3)   #  Set of Modules, change this number to change the number of modules
W = range(10)   # Set of Wafers per Module, change this number to change the number of wafers

# Define Sub Sets 
recipe_steps = {1} # Set of process steps where all wafers belonging to a specific run of a module are processed together during a recipe step.
I_recipe = recipe_steps # renamed name for consistency
I_load = set(recipe_step -1 for recipe_step in recipe_steps)
I_unload = set(recipe_step +1 for recipe_step in recipe_steps)

I_automation = {0,2}
# T(i,j) is simply the duration of a process step. T is not wafer dependent. This constraint is imposed to simplify the model and means that processing in the automation module is not affected by the order in which wafers are loaded and unloaded from different stations.
# Randomly generate durations between 10 and 100 seconds depending on the process step i and module j

if __name__ == '__main__':
    # Set the duration of process step 4 for module 0 to 100 seconds, just for test purposes.
    T = {(i, j): np.random.randint(10, 100) for i in I for j in J}
    # Überschreibt die Werte in T für alle Paare (1, j) mit neuen zufälligen Werten zwischen 1000 und 2000
    T.update({(1, j): np.random.randint(1000, 2000) for j in J if (1, j) in T})
    with open('T(i,j).csv', 'w', newline='') as file:
        writer = csv.writer(file)
        print("\n".join([f"T[{i}][{j}] = {T[i, j]}" for i in I for j in J]))
        [writer.writerow({T[i, j]}) for i in I for j in J]

    # Randomly generate transfert times
    T_Trans = {(k, l, x, i, j, w): np.random.randint(10, 15) for k in I_automation for l in J for x in W for i in I_automation for j in J for w in W if not (l == j and x == w) and not (k == i and l == j)}
    with open('T_Trans.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        print("\n".join([f"T_Trans[{k},{l},{x},{i},{j},{w}] = {T_Trans[k, l, x, i, j, w]}" for k in I_automation for l in J for x in W for i in I_automation for j in J for w in W if (k, l, x) < (i, j, w) and not (l == j and x == w) and not (k == i and l == j)]))
        [writer.writerow({T_Trans[k, l, x, i, j, w]}) for k in I_automation for l in J for x in W for i in I_automation for j in J for w in W if not (l == j and x == w) and not (k == i and l == j)]

    # Ramdomly generateted capacipties for all process modules between 5 and 10
    C = {j: np.random.randint(5, 10) for j in J}
    # set the first capacity to 5, just for test purposes.
    C[0] = 5
    with open('C(j).csv', 'w', newline='') as file:
        writer = csv.writer(file)
        print("\n".join([f"C[{j}] = {C[j]}" for j in J for i in I]))
        [writer.writerow({C[j]}) for j in J for i in I]


def read_T_from_csv(filename, I, J):
    # Initialize an empty dictionary to store the triple indexed values
    T_list = []
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read each line
        for line in file:
            txt = line.strip().replace('\n','')
            T_list.append(float(txt))
    line = 0
        # Convert the line to an integer and append it to the list
    T = {}
    for i in I:
        for j in J:
                T[(i, j)] = T_list[line]
                line += 1 
    return T
def read_C_from_csv(filename):
    # Initialize an empty dictionary to store the triple indexed values
    C = []
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read each line
        for line in file:
            txt = line.strip().replace('\n','')
            C.append(float(txt))
    return C
def read_T_Trans_from_csv(filename):
    # Initialize an empty list to store the values
    T_Trans_list = []
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read each line
        for line in file:
            txt = line.strip().replace('\n','')
            T_Trans_list.append(float(txt))
    line = 0
    # Initialize an empty dictionary to store the values
    T_Trans = {}
    for k in I_automation:
        for l in J:
            for x in W:
                for i in I_automation:
                    for j in J:
                        for w in W:
                            if not (l == j and x == w) and not (k == i and l == j):
                                T_Trans[(k, l, x, i, j, w)] = T_Trans_list[line]
                                line += 1 
    return T_Trans

C = read_C_from_csv('C(j).csv')
T = read_T_from_csv('T(i,j).csv', I, J)
T_Trans = read_T_Trans_from_csv('T(k,l,x,i,j,w)_Trans.csv')
# Print generated T and C

print("Durations for each step:", T)
print("Capacities for each module:", C)
# print(("Transition between two steps:", T_Trans))

