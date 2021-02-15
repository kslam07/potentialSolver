from pathlib import Path
import numpy as np
from potentialSolver.potentialSolver.discreteVortexMethod import \
    compute_circulation

class Airfoil:

    def __init__(self, npanels, eps, datafile, airfoil_type):
        """
        :param float npanels: number of panels
        :param float eps: argument for parabolic airfoils (for a test case in
        Katz and Plotkins)
        :param str datafile: file containing the airfoil
        :param str airfoil_type: must either be "NACA" or "parabolic"
        """

        self.npanels = npanels
        self.eps = eps
        self.datapath = Path(__file__).parent.parent / 'data'
        self.airfoil_type = airfoil_type
        self.datafile = self.generate_airfoil(datafile)

    def generate_airfoil(self, filename):
        """
        Load file containing airfoil geometry, compute the surface / camberline
        shape.
        Note that the vortex points are located at the quarter-chord point of
        each panel and
        that the collocation points are located at the three-quarter point of
        each panel.
        :return: 2D array with 6 columns consisting of: x location of panel, y
        location of panel,
        x location of vortex, y location of vortex, x location of collocation
        point, y location of collocation point, panel inclination.
        """

        # Open data file with naca details
        with open(self.datapath / filename) as f:
            contents = f.readlines()[1:]
        # Converts string into floats for x and y location of airfoil
        for index, line in enumerate(contents):
            contents[index] = line.strip('\n')
            contents[index] = ' '.join(line.split()).split(' ')
            contents[index][0] = float(contents[index][0])
            contents[index][1] = float(contents[index][1])

        # compute end points (in x and y) for each panel
        xloc, yloc = self._compute_panels(filename, self.airfoil_type)

        # computes inclination angle for panels in radians
        alpha = self.compute_inclination(xloc, yloc)

        # compute vortex element and collocation point location for each panel
        x_1, y_1, x_3, y_3 = self.compute_panelpoints(xloc, yloc)

        # computee the chord length per panel
        chord_length = self._compute_panel_length(xloc, yloc)

        # combine everything into a list
        combined = np.array([xloc, yloc, x_1, y_1, x_3, y_3, alpha,
                             chord_length])

        # x,y panel, x,y vortex, x,y collocation point, alpha, panel length
        return combined

    def _compute_panels(self, filename, airfoil_type):

        # Compute coordinates of the panels
        xloc = np.linspace(0, 1, self.npanels + 1)  # N+1 points for N panels

        # Check if airfoil is cambered
        yloc = []

        if airfoil_type == 'parabolic':
            for i in xloc:
                yloc.append(self.parabolic(i))

        if airfoil_type == 'naca':
            if int(filename[4:8][0]) == 0:  # Checks if airfoil is symmetric
                yloc = np.zeros(len(xloc))
            else:
                for i in xloc:
                    # Analytical based on p criteria p=location of max camber
                    if i < int(filename[4:8][1]) / 10:
                        yloc.append(self.naca_camber1(i, filename))
                    else:
                        yloc.append(self.naca_camber2(i, filename))

        return xloc, np.array(yloc)

    def naca_camber1(self, x, filename):
        # equation if x<p
        # m is the first of the four digits
        # p is the second of the four digits
        m = int(filename[4:8][0]) / 100  # m is the maximum camber
        p = int(filename[4:8][1]) / 10  # p is the position of maximum camber
        return m / p ** 2 * (2 * p * x - x ** 2)

    def naca_camber2(self, x, filename):
        # Equation if x>p
        m = int(filename[4:8][0]) / 100  # m is the maximum camber
        p = int(filename[4:8][1]) / 10  # p is the position of maximum camber
        return m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x ** 2)

    def parabolic(self, xloc):
        return 4 * self.eps * xloc * (1 - xloc)

    def compute_inclination(self, x_panel, y_panel):
        """
        Compute the panel inclination for each panel

        :return: 1D array of the panel inclination in RAD
        """
        x_roll = np.roll(x_panel, -1)  # Shift indices one to the left
        y_roll = np.roll(y_panel, -1)

        # The last value is zero and should not be used
        alpha = np.arctan((y_panel - y_roll) / (x_roll - x_panel))
        return alpha

    def compute_panelpoints(self, x_panel, y_panel):
        """
        Computes the vortex point (quarter point) and collocation point
        (three quarter point)
        :param ndarray x_panel: 1D-array containing the x-vertices of panels
        :param ndarray y_panel: 1D-array containing the y-vertices of panels
        :return: x and y location of the quarter line point and three quarter
        point, i.e. the vortex and collocation point, respectively.
        """
        x_roll = np.roll(x_panel, -1)
        y_roll = np.roll(y_panel, -1)

        x_1 = x_panel * (3 / 4) + x_roll * (1 / 4)
        y_1 = y_panel * (3 / 4) + y_roll * (1 / 4)

        x_3 = x_panel * (1 / 4) + x_roll * (3 / 4)
        y_3 = y_panel * (1 / 4) + y_roll * (3 / 4)

        return x_1, y_1, x_3, y_3

    def _compute_panel_length(self, xpanel, ypanel):

        # x-y coordinates array of the panels are shifted one position to the
        # left. Subtracting with the original
        # x-y coordinates gives dx and dy from which we obtain the
        # "chord" / panel length
        x_roll = np.roll(xpanel, -1)
        y_roll = np.roll(ypanel, -1)

        # Note: last element of array is never used; so it's fine like this
        chord_length = np.sqrt((xpanel - x_roll) ** 2 + (ypanel - y_roll) ** 2)

        return chord_length

    def run(self, aoa, q_inf, density=1.225, deg=True):
        """
        Run the discrete vortex panel method.

        :param float aoa: angle of attack of the airfoil
        :param float q_inf: freestream velocity NOTE: not the dynamic pressure!
        :param float density: density of the flow
        :param boolean deg: the angle of attack is assumed to be degrees
        if True, else assumed to be in radians
        :return: 2D array with rows containing the circulation at each panel
        and columns the angle of attack of the run
        :rtype: ndarray
        """

        if deg:
            _aoa = np.radians(aoa)
        else:
            _aoa = aoa

        # run the discrete vortex method;
        # theory given in Katz and Plotkins, Ch. 11.1.1
        circ_arr = compute_circulation(_aoa, q_inf, self.datafile)

        # compute secondary parameters
        results = self.compute_parameters(self.datafile, circ_arr, q_inf,
                                          density)

        self.results = results

        return results

    def compute_parameters(self, airfoil_data, circ_arr, q_inf, density=1.225):
        """
        Compute the secondary parameters such as pressure (dcp)  and lift (dcl)
        difference(!) along the airfoil (x/c)

        :param circ_per_aoa: 1D array containing the circulation at each panel
        of the discretized airfoil
        :return: 1D array containing the secondary parameters
        :rtype: list
        """

        p_dyn = 0.5 * density * q_inf ** 2  # compute the dynamic pressure
        dcl = density * q_inf * circ_arr / p_dyn
        # last row of airfoil_data holds the chord length
        dcp = density * q_inf * circ_arr / airfoil_data[-1, :-1] / p_dyn

        return np.array([circ_arr, dcl, dcp])


if __name__ == "__main__":
    from potentialSolver.potentialSolver.postProcess import plot_results

    params = {"npanels": 100, "eps": 1.0, "datafile": "naca2414.txt",
              "airfoil_type": "naca"}

    testfoil = Airfoil(**params)

    testfoil.run(5, 1)

    fig, ax = plot_results(testfoil)

    fig.show()
