import numpy as np

weather = [5, 25, 50, 75, 95]

am_base = np.genfromtxt("output/ACT_30_1000_GHz_el60_annual_05.txt")

am_tau = am_base[:,0]
am_T = am_base[:,0]


for pwv in weather:
    am = np.genfromtxt(f"output/ACT_30_1000_GHz_el60_annual_{pwv:02d}.txt")
    am_tau = np.column_stack((am_tau, am[:,1]))
    am_T = np.column_stack((am_T, am[:,2]))

np.savetxt("am_ACT_tau_annual.txt", am_tau)
np.savetxt("am_ACT_T_annual.txt", am_T)
