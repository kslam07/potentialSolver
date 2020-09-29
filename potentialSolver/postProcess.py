"""
Functions created for plotting
"""
from potentialSolver.airfoil import Airfoil
import matplotlib.pyplot as plt

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

filename='NACA2414.txt'
data=Airfoil(25,1,'NACA2414.txt')
plot_airfoil(data)