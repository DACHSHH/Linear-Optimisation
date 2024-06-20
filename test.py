from data import *
y= 0
for k in I_automation:
    for l in J:
        for x in W:
            for i in I_automation:
                for j in J:
                    for w in W:
                        if (k, l, x) < (i, j, w) and not (l == j and x == w) and not (k == i and l == j): # avoids comparing the same process steps twice and avoids comparing two steps of the same wafer (j,w) because (2) already holds and avoids comparing the same process module in its same process step because (3) holds.
                               print(i,j,w,k,l,x)
                               y= y+ 1
print('y ist = ',y)


import matplotlib.pyplot as plt
import numpy as np

# Daten generieren
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Erstellen Sie eine Figur und zwei Subplots
fig, (ax1, ax2) = plt.subplots(2, 1)

# Zeichnen Sie den ersten Plot
ax1.plot(x, y1, color='blue')
ax1.set_title('Sinus-Plot')

# Zeichnen Sie den zweiten Plot
ax2.plot(x, y2, color='red')
ax2.set_title('Cosinus-Plot')

# Anzeigen der Figur
plt.tight_layout()
plt.show()