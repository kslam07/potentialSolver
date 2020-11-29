import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from potentialSolver.airfoil import Airfoil

def reader():
    with open(Path(__file__).parent.parent / 'data' / filename) as f:
        contents = f.readlines()[1:]
        for index, line in enumerate(contents):  # Converts string into floats for x and y location of airfoil
            contents[index] = line.strip('\n').split('\t')
            contents[index] = ' '.join(line.split()).split(' ')
    return contents

filename='naca0012.txt'
x = reader()

x_loc = np.loadtxt(Path(__file__).parent.parent/ 'data' / 'xloc_naca0012.txt')


xloc = []
pressure = []
for i in range(31):
    xloc.append(int(x[i][0]))
    pressure.append(float(x[i][1]))
for i in range(31):
    xloc.append(int(x[i][2]))
    pressure.append(float(x[i][3]))
for i in range(31, 35):
    xloc.append(int(x[i][0]))
    pressure.append(float(x[i][1]))

# print ([i-31 for i in xloc if i>31])

aoa = 4
eps = 0.1

params = {"npanels": 50, "eps": 0.1, "datafile": "naca0015.txt", "airfoil_type": "naca"}
parabolic = Airfoil(**params)
#parabolic.run(aoa, 1)

#plot_results(parabolic, aoa, eps)

airfoil=Airfoil(**params)
airfoil.run(aoa,1)
xcol = airfoil.datafile[4, :-1]

plt.plot(x_loc, -1 * np.array(pressure[31:]), label='experimental data',marker='x',ls='')
plt.plot(xcol, airfoil.results[-1],label='numerical solution')
plt.xlabel('x/c')
plt.ylabel(r'$C_p$')
plt.legend()