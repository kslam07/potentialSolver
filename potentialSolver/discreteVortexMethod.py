"""
Contains the discrete vortex method for the thin airfoil theory
"""
import numpy as np

def lumpvor2d(xcol, zcol, xvor, zvor, circvor=1):
    """
    Compute the velocity at an arbitrary collocation point (xcol, zcol) due to vortex element of circulation circvor,
    placed at (xvor, zvor).

    :param circvor:
    :param xcol:
    :param ycol:
    :param xvor:
    :param yvor:

    :return: 1D array containing the velocity vector (u, w) (x-comp., z-comp.)
    :rtype: ndarray

    """

    # Compute the radius vector from the collocation point to the vortex element

    # some algebra

    return NotImplementedError


def normal_vector(alpha_i):
    """
    Compute the normal vector of the vortex element (xvor, zvor) on each panel (at collocation point).

    :param alphai: 1D array of the panel inclination of each panel (computed at the collocation point on each panel)

    :return: 1D array containing the normal vectors at the collocation of each panel
    """
    return NotImplementedError


def tangent_vector(alpha_i):
    """
    Compute the normal vector of the vortex element (xvor, zvor) on each panel (at collocation point).

    :param alphai: 1D array of the panel inclination of each panel (computed at the collocation point on each panel)

    :return: 1D array containing the tangent vectors at the collocation of each panel
    """
    return NotImplementedError


def compute_circulation():
    """
    Compute the circulation at each collocation point

    :return: 1D array containing the circulation at each collocation point (size equal to number of panels).
    """

    # compute RHS

    # compute discretization matrix

    # compute state vector

    return NotImplementedError

