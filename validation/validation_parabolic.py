from potentialSolver.airfoil import Airfoil
import numpy as np
import matplotlib.pyplot as plt
from potentialSolver.airfoil import Airfoil


def dCp(x, aoa, epsilon):
    return (4 * np.sqrt((1-x)/x) * np.deg2rad(aoa) + 32 * epsilon * np.sqrt(x * (1-x)))

def plot_results(airfoil, aoa, eps):

    # retrieve x-position of collocation point
    xcol = airfoil.datafile[4, :-1]
    ycol = dCp(xcol, aoa, eps)

    fig, ax = plt.subplots(1, 2)

    ax[0].plot(xcol, airfoil.results[-1], label="pressure diff.")
    ax[0].plot(xcol, dCp(xcol, aoa, eps))
    ax[1].plot(xcol, airfoil.results[-2], label="lift diff.")

    ax[0].set_xlim(left=0, right=1)
    ax[1].set_xlim(left=0, right=1)
    ax[0].legend()
    ax[1].legend()

    return fig, ax

aoa = 10
eps = 0.1

params = {"npanels": 20, "eps": 0.1, "datafile": "naca0010.txt", "airfoil_type": "parabolic"}
parabolic = Airfoil(**params)
parabolic.run(aoa, 1)

plot_results(parabolic, aoa, eps)
