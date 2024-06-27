import numpy as np
import csv

# Define sets
I = range(5)  # Set of Process Steps, change this number to change the number of process steps
J = range(3)   #  Set of Modules, change this number to change the number of modules
W = range(10)   # Set of Wafers per Module, change this number to change the number of wafers

# Define Sub Sets 
recipe_steps = {2} # Set of process steps where all wafers belonging to a specific run of a module are processed together during a recipe step.
I_recipe = recipe_steps # renamed name for consistency
I_load = set(recipe_step - 1 for recipe_step in recipe_steps)
I_unload = set(recipe_step + 1 for recipe_step in recipe_steps)

I_automation = {1,3}
I_casette = {0,4}
# Module Positions
def get_T_Trans_condition(k,i):
    return not(i in I_casette or k in I_casette) and k not in I_recipe and i not in I_recipe    # No Transfer Time if i == 0 or k == 0 or to start a recipe


def get_T_Trans(k, l, i, j):
    # 
    dphi = 90
    phi__position = [90, 180, -90] # -180 < phi <= 180
    phi_last = 0
    phi_start = 0
    if k in I_unload:
        phi_start = phi__position[l]
    if i in I_load:
        phi_last = phi__position[j]
    phi_delta =  abs(min(abs(phi_start) - abs(phi_last), abs(phi_last) - abs(phi_start)))
    if phi_start != phi_last and abs(phi_start) == abs(phi_last):
        phi_delta = 180
    T_Trans = phi_delta/dphi # positive and negative rotations are possible
    return T_Trans

if __name__ == '__main__':
    # T(i,j) is simply the duration of a process step. T is not wafer dependent. This constraint is imposed to simplify the model and means that processing in the automation module is not affected by the order in which wafers are loaded and unloaded from different stations.
    
    # Randomly generate durations between 10 and 100 seconds depending on the process step i and module j
    T = {(i, j): np.random.randint(50, 100) for i in I for j in J}
    # Überschreibt die Werte in T für alle Paare (1, j) mit neuen zufälligen Werten zwischen 1000 und 2000
    T.update({(i, j): np.random.randint(1000, 2000) for i in I_recipe for j in J if (i, j) in T})
    T.update({(i, j): 100 for i in I_casette for j in J if (i, j) in T})
    with open('Data\T(i,j).csv', 'w', newline='') as file:
        writer = csv.writer(file)
        print("\n".join([f"T[{i}][{j}] = {T[i, j]}" for i in I for j in J]))
        [writer.writerow({T[i, j]}) for i in I for j in J]

    # Randomly generates transfert times
    T_Trans = {(k, l, i, j): get_T_Trans(k, l, i, j)
               for k in I for l in J
               for i in I for j in J
               if get_T_Trans_condition(k,i)}
    with open('Data\T(k,l,i,j)_Trans.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        print("\n".join([f"T_Trans[{k},{l},{i},{j}] = {T_Trans[k, l, i, j]}" for k in I for l in J for i in I for j in J if get_T_Trans_condition(k,i)]))
        [writer.writerow({T_Trans[k, l, i, j]}) for k in I for l in J for i in I for j in J if get_T_Trans_condition(k,i)]

    # Ramdomly generateted capacipties for all process modules between 5 and 10
    C = {j: np.random.randint(5, 10) for j in J}
    # set the first capacity to 5, just for test purposes.
    C[0] = 5
    with open('Data\C(j).csv', 'w', newline='') as file:
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
    for k in I:
        for l in J:
            for i in I:
                for j in J:
                    if get_T_Trans_condition(k,i):
                        T_Trans[(k, l,i, j)] = T_Trans_list[line]
                        line += 1 
    return T_Trans

C_Casette = len(J) * len(W) 
C = read_C_from_csv('Data\C(j).csv')
T = read_T_from_csv('Data\T(i,j).csv', I, J)
T_Trans = read_T_Trans_from_csv('Data\T(k,l,i,j)_Trans.csv')
# Print generated T and C

print("Durations for each step:", T)
print("Capacities for each module:", C)
# print(("Transition between two steps:", T_Trans))

