"""
Functions created for plotting
"""
from potentialSolver.airfoil import Airfoil
import matplotlib.pyplot as plt
import numpy as np

def plot_airfoil(airfoil):
    # plot for test
    xloc, yloc, x_1, y_1, x_3, y_3, alpha = airfoil.datafile
    plt.scatter(x_1[:-1], y_1[:-1])
    plt.scatter(x_3[:-1], y_3[:-1])
    plt.plot(xloc, yloc, marker='x')
    plt.axis('scaled')
    # plt.ylim(0,2*max(yloc))
    plt.grid()
    plt.show()
    return


def plot_dcp(airfoil):

    # retrieve x-position of collocation point
    xcol = airfoil.datafile[2, :-1]

    # retrieve chord length
    chord_length = np.cumsum(airfoil.datafile[-1, :-1])

    # compute x/c
    x_per_c = xcol / chord_length

    fig, ax = plt.subplots(1, 1)

    ax.plot(x_per_c, airfoil.results[-1])

    return fig, ax
