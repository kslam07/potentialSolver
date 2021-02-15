from potentialSolver.potentialSolver.airfoil import Airfoil
import numpy as np
import matplotlib.pyplot as plt

params = {"npanels": 10, "eps": 0.1, "datafile": "NACA0015.txt", "airfoil_type": "naca"}

testfoil = Airfoil(**params)

testfoil.run(5, 1)

params = {"npanels": 25, "eps": 0.1, "datafile": "NACA0015.txt", "airfoil_type": "naca"}

test = Airfoil(**params)

test.run(5, 1)

params = {"npanels": 100, "eps": 0.1, "datafile": "NACA0015.txt", "airfoil_type": "naca"}

t3 = Airfoil(**params)

t3.run(5, 1)

fig,ax=plt.subplots(1,2)
ax[0].plot(testfoil.datafile[4, :-1],testfoil.results[-1],label='n=`10')
ax[1].plot(testfoil.datafile[4, :-1],testfoil.results[-2],label='n=10')
ax[0].plot(test.datafile[4, :-1],test.results[-1],ls='dotted',label='n=25')
ax[1].plot(test.datafile[4, :-1],test.results[-2],ls='dotted',label='n=25')
ax[0].plot(t3.datafile[4, :-1],t3.results[-1],ls='dotted',label='n=100')
ax[1].plot(t3.datafile[4, :-1],t3.results[-2],ls='dotted',label='n=100')
#ax[0].set_title(r'$\Delta$P over x/c')
#ax[1].set_title(r'$\Delta$L over x/c')
ax[0].set_xlabel('x/c')
ax[0].set_ylabel(r'$\Delta$P')
ax[1].set_xlabel('x/c')
ax[1].set_ylabel(r'$\Delta$L')
ax[0].legend()
ax[1].legend()