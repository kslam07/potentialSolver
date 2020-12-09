from potentialSolver.airfoil import Airfoil

import numpy as np
import matplotlib.pyplot as plt

aoa_arr = np.arange(0, 10.5, 0.5)

npanels = 50  # number of panels
density = 1.225  # density [kg/m3]
q_inf = 1.0  # free-stream velocity

# init some arrays to store results
results_2414 = np.zeros((1, npanels))
results_0010 = np.zeros((1, npanels))

naca0010 = Airfoil(npanels, 1, datafile="naca0010.txt", airfoil_type="naca")
naca2414 = Airfoil(npanels, 1, datafile="naca2414.txt", airfoil_type="naca")

for aoa in aoa_arr:
    foil_results = Airfoil(npanels, 1, datafile="naca2414.txt", airfoil_type="naca").run(aoa, q_inf=q_inf,
                                                                                         density=density)
    results_2414 = np.vstack((results_2414, foil_results))

for aoa in aoa_arr:
    foil_results = Airfoil(npanels, 1, datafile="naca0010.txt", airfoil_type="naca").run(aoa, q_inf=q_inf,
                                                                                         density=density)
    results_0010 = np.vstack((results_0010, foil_results))

results_2414 = results_2414[1:]
results_0010 = results_0010[1:]

# compute Cl for each run
cla_0010 = np.sum(results_0010[1::3], axis=1)
cla_2414 = np.sum(results_2414[1::3], axis=1)

fig_dcp, ax_dcp = plt.subplots(1, 3, dpi=150)

aoa_i = 5

ax_dcp[0].plot(naca0010.datafile[4, :-1], results_0010[aoa_i*6-1, :], label=r"NACA0010 ", c='r')  # xcol vs dCp
ax_dcp[0].plot(naca2414.datafile[4, :-1], results_2414[aoa_i*6-1, :], label=r"NACA2414", c='b')  # xcol vs dCp
ax_dcp[0].legend()
ax_dcp[0].set_title(r"$\Delta C_{p}$ at $\alpha$ = $5^\circ$")
ax_dcp[0].set_xlabel("x/c [-]")
ax_dcp[0].set_ylabel(r"$\Delta C_{p}$ [-]")
ax_dcp[0].grid()

ax_dcp[1].plot(naca0010.datafile[4, :-1], results_0010[-1], label=r"NACA0010", c='r')  # xcol vs dCp
ax_dcp[1].plot(naca2414.datafile[4, :-1], results_2414[-1], label=r"NACA2414", c='b')  # xcol vs dCp
ax_dcp[1].set_title(r"$\Delta C_{p}$ at $\alpha$ = $10^\circ$")
ax_dcp[1].set_xlabel("x/c [-]")
ax_dcp[1].set_ylabel(r"$\Delta C_{p}$ [-]")
ax_dcp[1].grid()

ax_dcp[2].plot(aoa_arr, cla_0010, label=r"NACA0010", c='r')
ax_dcp[2].plot(aoa_arr, cla_2414, label=r"NACA2414", c='b')
ax_dcp[2].set_title(r"$C_{L_{\alpha}}$ vs. AoA")
ax_dcp[2].set_xlabel(r"$\alpha$ [$^\circ$]")
ax_dcp[2].set_ylabel(r"$C_{l}$ [-]")
ax_dcp[2].grid()

#fig_dcp.suptitle(r"Comparison between NACA0010 and NACA2414")