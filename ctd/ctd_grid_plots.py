import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/time/';
deployment_name = 'deploy2_';
measurement_type = 'ctd_grid_';
file_type = 'raw_'
profile_array = [];
pressure_array = [];
temperature_array = [];
salinity_array = [];

for i in range(0,10,2):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	pressure_array.extend(c_data["c_pres"].tolist())
	temperature_array.extend(c_data["c_temp"].tolist())
	salinity_array.extend(c_data["c_sal"].tolist())
	profile_array.extend([i]*len(c_data["c_sal"].tolist()))

neg_pressure_array = [-x for x in pressure_array]

#Creating a grid
xi,yi = np.meshgrid(np.arange(0,10,0.25),np.arange(-120,0,1))
grid_salinity = griddata((profile_array,neg_pressure_array),salinity_array,(xi,yi),method='linear')
grid_temperature = griddata((profile_array,neg_pressure_array),temperature_array,(xi,yi),method='linear')

#Salinity plot
plt.subplot(121)
plt.scatter(xi,yi,s=4,c=grid_salinity)
plt.title('Salinity (pss)')
plt.xlabel('Profile')
plt.ylabel('Pressure (dbar)')
plt.colorbar()

#Temperature plot
plt.subplot(122)
plt.scatter(xi,yi,s=4,c=grid_temperature)
plt.title('Temperature (pss)')
plt.xlabel('Profile')
plt.colorbar()
plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
#plt.show()