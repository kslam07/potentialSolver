"""
Contains the discrete vortex method for the thin airfoil theory
"""

import numpy as np


def lumpvor2d(xcol, zcol, xvor, zvor, circvor=1):
    """
    Compute the velocity at an arbitrary collocation point (xcol, zcol) due
    to vortex element of circulation circvor, placed at (xvor, zvor).

    :param xcol: x-coordinate of the collocation point
    :param zcol: z-coordinate of the collocation point
    :param xvor: x-coordinate of the vortex
    :param zvor: z-coordinate of the vortex
    :param circvor: circulation strength of the vortex (base units)

    :return: 1D array containing the velocity vector (u, w) (x-comp., z-comp.)
    :rtype: ndarray

    """

    # transformation matrix for the x, z distance between two points
    dcm = np.array([[0, 1],
                    [-1, 0]])

    # magnitude of the distance between two points
    r_vortex_sq = (xcol - xvor) ** 2 + (zcol - zvor) ** 2

    # the distance in x, and z between two points
    dist_vec = np.array([xcol - xvor, zcol - zvor])

    norm_factor = circvor / (2.0 * np.pi * r_vortex_sq)  # circulation at
    # vortex element / circumferential distance

    # induced velocity of vortex element on collocation point
    vel_vor = norm_factor * dcm @ dist_vec

    return vel_vor


def normal_vector(alpha_i):
    """
    Compute the normal vector of the vortex element (xvor, zvor) on each
    panel (at collocation point).

    :param alpha_i: 1D array of the panel inclination of each panel (
    computed at the collocation point on each panel)

    :return: 1D array containing the normal vectors at the collocation of each
    panel
    """

    # transpose because created array is (2, len(alpha_i))
    return np.array([np.sin(alpha_i), np.cos(alpha_i)]).T


def tangent_vector(alpha_i):
    """
    Compute the normal vector of the vortex element (xvor, zvor) on each panel
    (at collocation point).

    :param alpha_i: 1D array of the panel inclination of each panel
    (computed at the collocation point on each panel)

    :return: 1D array containing the tangent vectors at the collocation of each
    panel
    """

    # transpose because created array is (2, len(alpha_i))
    return np.array([np.cos(alpha_i), -np.sin(alpha_i)]).T


def compute_circulation(aoa, q_inf, airfoil_data):
    """
    Compute the circulation at each collocation point

    :return: 1D array containing the circulation at each collocation point
    (size equal to number of panels).
    """

    # "copy" values from airfoil array
    colcoords = airfoil_data[[4, 5], :-1].T
    vorcoords = airfoil_data[[2, 3], :-1].T
    alpha_i = airfoil_data[6, :-1]  # remove last element as it is a dummy file

    # compute the free-stream velocity component
    u_inf, w_inf = np.cos(aoa) * q_inf, np.sin(aoa) * q_inf

    n_vecs = normal_vector(alpha_i)

    rhs = []
    coeff_infl = []

    # builds the influence coefficient matrix and RHS vector to solve for
    # circulation at each collocation point
    for (xcol, zcol), n_vec in zip(colcoords, n_vecs):

        # compute RHS
        rhs.append(-np.array([u_inf, w_inf]) @ n_vec)  # this will be a scalar

        # computes the induced normal velocity (Vn) at a collocation point due
        # to all vortex elements
        for xvor, zvor in vorcoords:
            # induced Vn of a vortex element on collocation point
            vel_vor = lumpvor2d(xcol, zcol, xvor, zvor)
            coeff_infl.append(vel_vor @ n_vec)  #compute influence coefficients

    # reshape coeff. infl list into the correctly-shaped matrix
    # matrix should be length colcoords and width vorcoords
    discmatrix_shape = (len(colcoords), len(vorcoords))
    coeff_infl = np.array(coeff_infl).reshape(discmatrix_shape)

    # convert RHS list to 1D array
    rhs_arr = np.array(rhs)

    # compute state vector, i.e. the circulation at each collocation point
    circ_arr = np.linalg.inv(coeff_infl) @ rhs_arr  # A^(-1) RHS

    return circ_arr
