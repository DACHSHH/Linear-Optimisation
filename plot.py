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
        

def plot_results(t, I, J, W):
    # Plot the solution
    # Initialize the figure and axes
    fig, axs = plt.subplots(len(J),1)
    # fig, axs = plt.subplots(2,1)
    ############################# Plot the solution ################################

    # Plot for each wafer
    
    for j in J:
        # if j == 0: # process module 0, comment out if you want to plot other process modules
        colors = plt.cm.tab20.colors
        handles = []
        labels = []
        for w in W:
            t_values = [t[(i, j, w)] for i in I]
            
            steps =  [i for i in range(len(t_values))]
            steps.insert(0,0)
            t_values.append(t_values[-1])
            axs[j].step(t_values, steps, color=colors[w % C[j]], label=f"Wafer {j,w}")
            handles.append(plt.Rectangle((0,0),1,1,color=colors[w % C[j]]))
            labels.append(f"Wafer {j,w}")
            # Set labels and show the plot
        axs[j].set_xlabel("Time")
        axs[j].set_ylabel("Process Step")
        # ax.invert_yaxis()
        axs[j].set_aspect('auto')
        axs[j].legend(handles=handles, labels=labels, bbox_to_anchor=(1.05, 1), loc='upper left') # Ajust sliders
        axs[j].set_xlim([0, 3000]) # improve!
  
            

    plt.tight_layout()
    plt.show() 

if __name__== "__main__":
    t = read_from_csv('results.csv', I, J, W)
    plot_results(t, I, J, W)
    
