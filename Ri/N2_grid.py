import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt
from N2_function import N2_function
from scipy.interpolate import griddata

outdir = '../../plots/Ri/N2/';
profile_array = []
pressure_array = []
N2_array = []
S2_array = []
Ri_array = []

for i in range(0,58,2):
	if i in [48,16,12,28]:
		pass#do nothing
	else:
		binned = N2_function(i)
		pressure_array.extend(binned.index.tolist())
		profile_array.extend([i]*len(binned.index))
		N2_array.extend(binned['N2'].tolist())
		S2_array.extend(binned['S2'].tolist())
		Ri_array.extend(binned['Ri'].tolist())

neg_pressure_array = [-x for x in pressure_array]
abs_N2_array = [(abs(x)) for x in N2_array]

xi,yi = np.meshgrid(np.arange(0,56,0.5),np.arange(-120,-10,0.5))
grid_N2 = griddata((profile_array,neg_pressure_array),abs_N2_array,(xi,yi),method='linear')
grid_S2 = griddata((profile_array,neg_pressure_array),S2_array,(xi,yi),method='linear')
grid_Ri = griddata((profile_array,neg_pressure_array),Ri_array,(xi,yi),method='linear')


plt.scatter(xi,yi,s=4,c=grid_N2)
#plt.scatter(profile_array,neg_pressure_array,s=10,c=abs_N2_array)
plt.title("Buoyancy Frequency")
plt.ylabel("Pressure (dbar)")
plt.xlabel("Profile")
plt.colorbar()

plt.savefig(outdir+'N2_grid'+".png")
plt.clf()

plt.scatter(xi,yi,s=4,c=grid_S2)
#plt.scatter(profile_array,neg_pressure_array,s=10,c=abs_N2_array)
plt.title("Shear Magnitude")
plt.xlabel("Profile")
plt.colorbar()
# plt.tick_params(
#     axis='y',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     left=False,      # ticks along the bottom edge are off
#     right=False,         # ticks along the top edge are off
#     labelleft=False) # labels along the bottom edge are off
plt.savefig(outdir+'S2_grid'+".png")
plt.clf()

plt.scatter(xi,yi,s=4,c=grid_Ri)
#plt.scatter(xi,yi,s=4,c=grid_Ri)
#plt.scatter(profile_array,neg_pressure_array,s=10,c=abs_N2_array)
plt.title("Richardson Number")
plt.xlabel("Profile")
plt.colorbar()
# plt.tick_params(
#     axis='y',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     left=False,      # ticks along the bottom edge are off
#     right=False,         # ticks along the top edge are off
#     labelleft=False) # labels along the bottom edge are off

plt.savefig(outdir+'Ri_grid'+".png")
plt.clf()

#plt.show()