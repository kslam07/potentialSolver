"""
Functions created for plotting
"""
from potentialSolver.airfoil import Airfoil
import matplotlib.pyplot as plt
import numpy as np

def plot_airfoil(airfoil):
    # plot for test
    xloc, yloc, x_1, y_1, x_3, y_3, alpha, __ = airfoil.datafile
    plt.scatter(x_1[:-1], y_1[:-1], label="collocation points")
    plt.scatter(x_3[:-1], y_3[:-1], label="vortex elements")
    plt.plot(xloc, yloc, marker='x', label="panel edges")
    plt.axis('scaled')
    plt.ylim(-5*max(yloc), 5*max(yloc))
    plt.grid()
    plt.legend()
    plt.show()
    return


def plot_results(airfoil):

    # retrieve x-position of collocation point
    xcol = airfoil.datafile[4, :-1]

    fig, ax = plt.subplots(1, 2)

    ax[0].plot(xcol, airfoil.results[-1], label="pressure diff.")
    ax[1].plot(xcol, airfoil.results[-2], label="lift diff.")

    ax[0].set_xlim(left=0, right=1)
    ax[1].set_xlim(left=0, right=1)
    ax[0].legend()
    ax[1].legend()

    return fig, ax