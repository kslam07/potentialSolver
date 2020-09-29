from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

class Airfoil:

    def __init__(self, npanels, eps, datafile):

        self.npanels = npanels
        self.eps = eps
        self.datapath = Path(__file__).parent.parent / 'data'
        self.datafile = self.generate_airfoil(datafile)



    def generate_airfoil(self, filename):
        """
        Load file containing airfoil geometry, compute the surface / camberline shape.
        Note that the vortex points are located at the quarter-chord point of each panel and
        that the collocation points are located at the three-quarter point of each panel.
        :return: 2D array with 6 columns consisting of: x location of panel, y location of panel,
        x location of vortex, y location of vortex, x location of collocation point,
        y location of collocation point, panel inclination.
        """

        with open(self.datapath / filename) as f:  # Open data file with naca details
            contents = f.readlines()[1:]
        for index, line in enumerate(contents):  # Converts string into floats for x and y location of airfoil
            contents[index] = line.strip('\n')
            contents[index] = ' '.join(line.split()).split(' ')
            contents[index][0] = float(contents[index][0])
            contents[index][1] = float(contents[index][1])
        coordinates = np.array(contents)  # Converts list to an array with the coordinates

        # compute collocation points for each panel

        xloc, yloc = self._compute_panels(self.npanels, filename)  # Computes x and y coordinates for the individual panels

        # compute panel inclinations

        alpha = self.compute_inclination(xloc, yloc)  # computes inclination angle for panels in radians

        # compute vortex element and collocation point location for each panel

        x_1, y_1, x_3, y_3 = self.compute_panelpoints(xloc, yloc)  # Returns x and y location for vortex point and collocation point

        # return xloc, yloc

        combined = np.array([xloc, yloc, x_1, y_1, x_3, y_3, alpha])  # combine everything into a list
        return combined


    def _compute_panels(self, npanels, filename):

        # Compute coordinates of the panels
        xloc=np.linspace(0, 1, self.npanels)

        # Check if airfoil is cambered
        yloc = []

        if int(filename[4:8][0]) == 0:  # Checks if airfoil is symmetric
            yloc = np.zeros(len(xloc))
        else:
            for i in xloc:
                if i < int(filename[4:8][1])/10:  # Analytical based on p criteria p=location of max camber
                    yloc.append(self.naca_camber1(i, filename))
                else:
                    yloc.append(self.naca_camber2(i, filename))

        return xloc, np.array(yloc)

    def naca_camber1(self, x, filename):
        # equation if x<p
        # m is the first of the four digits
        # p is the second of the four digits
        m = int(filename[4:8][0])/100  # m is the maximum camber
        p = int(filename[4:8][1])/10  # p is the position of maximum camber
        return m/p**2 * (2*p*x-x**2)

    def naca_camber2(self, x, filename):
        # Equation if x>p
        m = int(filename[4:8][0])/100  # m is the maximum camber
        p = int(filename[4:8][1])/10  # p is the position of maximum camber
        return m/(1-p)**2*((1-2*p)+2*p*x-x**2)

    def compute_inclination(self, x_panel, y_panel):
        """
        Compute the panel inclination for each panel

        :return: 1D array of the panel inclination in RAD
        """
        x_roll = np.roll(x_panel, -1)  # Shift indices one to the left
        y_roll = np.roll(y_panel, -1)
        alpha = np.arctan((y_panel-y_roll)/(x_roll-x_panel))  # The last value is zero and should not be used
        return alpha

    def compute_panelpoints(self, x_panel, y_panel):
        """
        Computes the vortex point (quarter point) and collocation point (three quarter point)
        :param x_panel:
        :param y_panel:
        :return: x and y location of the quarter line point and three quarter point
        """
        x_roll = np.roll(x_panel, -1)
        y_roll = np.roll(y_panel, -1)

        x_1 = x_panel * (3/4) + x_roll * (1/4)
        y_1 = y_panel * (3/4) + y_roll * (1/4)

        x_3 = x_panel * (1/4) + x_roll * (3/4)
        y_3 = y_panel * (1/4) + y_roll * (3/4)

        return x_1, y_1, x_3, y_3

    def run(self, aoa, q_inf):
        """
        Run the discrete vortex panel method.
        :return: 2D array with rows containing the circulation at each panel and columns the angle of attack of the run
        :rtype: ndarray
        """

        return NotImplementedError


    def compute_parameters(self, circ_per_aoa):
        """
        Compute the secondary parameters such as pressure and lift diference along the airfoil (x/c)

        :param circ_per_aoa: 2D array containing the circulation at each panel of the discretized airfoil (ROWS) for
                             arbitrary AoA (COLUMNS)
        :return: List of 2D arrays containing the secondary parameters (ROWS) along the chord (x/c) (COLUMNS)
        :rtype: list
        """

        return NotImplementedError
