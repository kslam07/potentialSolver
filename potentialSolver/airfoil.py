class Airfoil:

    def __init__(self, npanels, eps, datafile):

        self.npanels = npanels
        self.eps = eps
        self.datafile = self.load_airfoil(datafile)


    def load_airfoil(self):
        """
        Load file containing airfoil geometry, compute the surface / camberline shape.
        Note that the vortex points are located at the quarter-chord point of each panel and
        that the collocation points are located at the three-quarter point of each panel.
        :return:
        """

        # compute collocation points for each panel

        # compute vortex element location for each panel

        # compute panel inclinations

        return NotImplementedError


    def compute_inclination(self):
        """
        Compute the panel inclination for each panel

        :return: 1D array of the panel inclination in RAD
        """

        return NotImplementedError

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
