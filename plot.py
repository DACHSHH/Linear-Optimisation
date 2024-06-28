from data import *
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.ticker import MaxNLocator


def read_from_csv(filename, I, J, W):
    # Initialize an empty dictionary to store the triple indexed values
    t_list = []
    # Open the file in read mode
    with open(filename, 'r') as file:
        # Read each line
        for line in file:
            txt = line.strip().replace('\n','')
            t_list.append(float(txt))
    line = 0
        # Convert the line to an integer and append it to the list
    t = {}
    for i in I:
        for j in J:
            for w in W:
                t[(i, j, w)] = t_list[line]
                line += 1 
    t_new_cycle = t_list[line]
    return t, t_new_cycle
    
        
# 20 Colors, should be at least len(W), for each wafer
colors = plt.cm.tab20.colors
def plot_results(t, I, J, W, T, I_automation, I_recipe):
    # Initialize the figure for per-module plots
    fig1, axs = plt.subplots(len(J), 1, figsize=(10, len(J) * 3))  # One subplot per module j
    
    # Ensure axs is iterable (important when len(J) == 1)
    if len(J) == 1:
        axs = [axs]
    # Plotting for each module
    for j in J:
        # Iterate over each wafer
        for w in W:
            # Plot each step for the current wafer
            for i in I:
                start_time = t[(i, j, w)]
                duration = T[(i, j)]
                end_time = start_time + duration
                t_values = [start_time, end_time]
                steps = [i, i]
                line, = axs[j].step(t_values, steps, where='post', color=colors[w % int(C[j])])
                
            # Add legend entry for each wafer only once
            line.set_label(f"Wafer {j, w}")
        # Set labels and customize subplot
        axs[j].set_xlabel("Time")
        axs[j].set_ylabel("Process Step")
        axs[j].set_title(f"Module {j}")
        axs[j].legend(loc='upper left', bbox_to_anchor=(1,1))  # Legend on the right side
        axs[j].set_xlim(left=0,right=t_new_cycle)
        # Stelle sicher, dass die Y-Achse nur Ganzzahlen zeigt
        axs[j].yaxis.set_major_locator(MaxNLocator(integer=True))
        
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.subplots_adjust(right=0.85)  # Make room for the legend
    plt.show()  # Display the first plot

    # Initialize a separate figure for all wafers
    fig2, axs2 = plt.subplots(2, 1, figsize=(10, 3))
    # Additional plot for all wafers with different colors, no legend
    for p in range(2):
        for w in W:
            for j in J:
                for i in I:
                    t_values = [t[(i, j, w)], t[(i, j, w)] + T[(i, j)]]
                    # Define steps based on i in automation or recipe
                    steps = []
                    if i in I_automation:
                        if p == 0:
                            steps = [f'Automation Module {j}', f'Automation Module {j}']
                        else:
                            steps = ['Automation Module', 'Automation Module']
                    elif i in I_recipe:
                        # Differentiating process modules based on j
                        steps = [f'Process Module {j+1}', f'Process Module {j+1}']
                    else:
                        steps = ['Casette Loading', 'Casette Loading']
                    axs2[p].step(t_values, steps, where='post', color=colors[hash((i, j, w)) % len(colors)], linewidth=2,  label=f"{i} {j} {w}")
        # Customize the all-wafer plot
        axs2[p].set_xlabel("Time")
        axs2[p].set_ylabel("Module")
        axs2[p].set_title("All Wafers Overview")
        axs2[p].set_xlim(left=0,right=t_new_cycle)
        axs2[p].set_xlim(left=0)
    # Cursor hinzufügen
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()  # Display the second plot

    
if __name__== "__main__":
    t, t_new_cycle = read_from_csv('t(i,j,w)_results.csv', I, J, W)
    print('The output of the cluster is',round((len(J)*len(W))*3600/t_new_cycle,3), 'Wafer per hour.')
    plot_results(t, I, J, W, T, I_automation, I_recipe)
    
