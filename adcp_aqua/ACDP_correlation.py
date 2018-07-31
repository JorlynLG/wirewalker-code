import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from beam2ENU import beam2ENU

directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_plots/';
deployment_name = 'deploy1_';
measurement_type = 'euler_';
file_type = 'raw_'

for i in range(1):
	a_file = 'A'+("%07d" % (i,))
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)

	a_vel1 = a_data["a_vel1"].values
	a_vel2 = a_data["a_vel2"].values
	a_vel3 = a_data["a_vel3"].values


	meanV1 = np.mean(a_vel1)
	stdV1 = np.std(a_vel1)
	meanV2 = np.mean(a_vel2)
	stdV2 = np.std(a_vel2)
	meanV3 = np.mean(a_vel3)
	stdV3 = np.std(a_vel3)	


	for i in range(len(a_vel1)):
		if (a_data["a_corr1"].values[i]<75 or a_data["a_corr2"].values[i]<75 or a_data["a_corr3"].values[i]<75):
			a_vel1[i] = np.nan
			a_vel2[i] = np.nan
			a_vel3[i] = np.nan
	for i in range(len(a_vel1)):
		if (abs(a_vel1[i]-meanV1)>=3*stdV1):
			a_vel1[i] = np.nan
	for i in range(len(a_vel2)):
		if (abs(a_vel2[i]-meanV2)>=3*stdV2):
			a_vel2[i] = np.nan
	for i in range(len(a_vel3)):
		if (abs(a_vel3[i]-meanV3)>=3*stdV3):
			a_vel3[i] = np.nan

plt.plot(a_data["a_vel3"].values)
plt.show()