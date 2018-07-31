import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/time/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_time_';
file_type = 'raw_'
profile_array = [];
pressure_array = [];
temperature_array = [];
salinity_array = [];

for i in range(0,58,2):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	pressure_array.extend(c_data["c_pres"].tolist())
	temperature_array.extend(c_data["c_temp"].tolist())
	salinity_array.extend(c_data["c_sal"].tolist())
	profile_array.extend([i]*len(c_data["c_sal"].tolist()))

neg_pressure_array = [-x for x in pressure_array]
plt.subplot(121)
plt.scatter(profile_array,neg_pressure_array,s=7,c=salinity_array)
plt.title('Salinity (pss)')
plt.xlabel('Profile')
plt.ylabel('Pressure (dbar)')

plt.subplot(122)
plt.scatter(profile_array,neg_pressure_array,s=7,c=temperature_array)
plt.title('Temperature (pss)')
plt.xlabel('Profile')

plt.savefig(outdir+measurement_type+deployment_name+".png")