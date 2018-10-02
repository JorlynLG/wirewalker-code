import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from beam2ENU import beam2ENU

directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_plots/';
deployment_name = 'deploy1_';
measurement_type = 'euler_';
file_type = 'raw_'

profile_array = [];
pressure_array = [];
up_array = [];
east_array = [];
north_array = [];

for i in range(0,58,2):
	a_file = 'A'+("%07d" % (i,))
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)
	a_data.index = pd.DatetimeIndex(a_data['a_time'])
	a_data = a_data.resample('S').mean()
	[east,north,up] = beam2ENU([a_data["a_beam1"][0],a_data["a_beam2"][0],a_data["a_beam3"][0],a_data["a_beam4"][0]],a_data['a_heading'].values,a_data['a_pitch'].values,a_data['a_roll'].values,a_data['a_vel1'].values,a_data['a_vel2'].values,a_data['a_vel3'].values)
	pressure_array.extend(range(len(east)))
	east_array.extend(east)
	north_array.extend(north)
	up_array.extend(up)
	profile_array.extend([i]*len(east))

neg_pressure_array = [-x for x in pressure_array]
plt.scatter(profile_array,pressure_array,s=1,c=up_array)
plt.colorbar()
plt.show()