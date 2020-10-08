# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:54:46 2020

@author: Thomas Verduyn
"""

import numpy as np
import matplotlib.pyplot as plt

def reader(filename):
    xc = []
    cp0 = []
    cp5 = []
    with open(filename) as f:
        contents = f.readlines()[1:]
    for index, line in enumerate(contents):  # Converts string into floats for x and y location of airfoil
        contents[index] = line.strip('\n').split()
        xc.append(float(contents[index][1]))
        cp0.append(float(contents[index][2]))
        cp5.append(float(contents[index][4]))
    return xc, cp0, cp5
        
filename = 'NACA0015_Reference_data.txt'
xc, cp0, cp5 = reader(filename)
plt.plot(xc,-np.array(cp5))
plt.plot(xc,-np.array(cp0))
plt.title(r'$\Delta$Cp over x/c')
plt.xlabel('x/c')
plt.ylabel(r'$\Delta Cp$')
plt.show()