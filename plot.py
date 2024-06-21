from functions import *
from data import *
import matplotlib.pyplot as plt

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
    return t
        

def plot_results(t, I, J, W, T, I_automation, I_recipe):
    # Initialize the figure for per-module plots
    fig1, axs = plt.subplots(len(J), 1, figsize=(10, len(J) * 3))  # One subplot per module j
    
    # Ensure axs is iterable (important when len(J) == 1)
    if len(J) == 1:
        axs = [axs]
    
    # Colors for each wafer
    colors = plt.cm.tab20.colors

    # Plotting for each module
    for index, j in enumerate(J):
        # Iterate over each wafer
        for w in W:
            # Plot each step for the current wafer
            for i in I:
                start_time = t[(i, j, w)]
                duration = T[(i, j)]
                end_time = start_time + duration
                t_values = [start_time, end_time]
                steps = [i, i]
                line, = axs[index].step(t_values, steps, where='post', color=colors[w % len(colors)], linewidth=2)

            # Add legend entry for each wafer only once
            line.set_label(f"Wafer {j, w}")

        # Set labels and customize subplot
        axs[index].set_xlabel("Time")
        axs[index].set_ylabel("Process Step")
        axs[index].set_title(f"Module {j}")
        axs[index].legend(loc='upper left', bbox_to_anchor=(1,1))  # Legend on the right side
        axs[index].set_xlim(left=0)

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.subplots_adjust(right=0.85)  # Make room for the legend
    plt.show()  # Display the first plot

    # Initialize a separate figure for all wafers
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 3))
    # Additional plot for all wafers with different colors, no legend
    for w in W:
        for j in J:
            for i in I:
                start_time = t[(i, j, w)]
                duration = T[(i, j)]
                end_time = start_time + duration
                t_values = [start_time, end_time]
                # Define steps based on i in automation or recipe
                if i in I_automation:
                    steps = ['Automation Module', 'Automation Module']
                elif i in I_recipe:
                    # Differentiating process modules based on j
                    steps = [f'Process Module {j+1}', f'Process Module {j+1}']
                ax2.step(t_values, steps, where='post', color=colors[hash((i, j, w)) % len(colors)], linewidth=2)

    # Customize the all-wafer plot
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Module")
    ax2.set_title("All Wafers Overview")
    ax2.set_xlim(left=0)

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()  # Display the second plot

if __name__== "__main__":
    t = read_from_csv('results.csv', I, J, W)
    plot_results(t, I, J, W, T, I_automation, I_recipe)
    
