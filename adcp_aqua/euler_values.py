import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_bins/';
deployment_name = 'deploy2_';
measurement_type = 'euler_';
file_type = 'raw_'
bin_number = 100

profile_array = [];
heading_array = [];
roll_array = [];
pitch_array = [];
time_array = []

for i in range(0,10,2):
	a_file = 'A'+("%07d" % (i,))
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)
	
	#Datetime binning
	#time = a_data["a_time"].values[:-(len(a_data["a_time"].values)%bin_number)].reshape(-1, bin_number)
	#time = [dt.datetime.strptime(x[:-6],"%Y-%m-%dT%H:%M:%S.%f") for x in time[:,int(bin_number/2)]]
	#time = [x.total_seconds() for x in time]

	heading_unwrap = np.unwrap(a_data["a_heading"].apply(np.radians).values)
	#heading= heading_unwrap[:-(len(heading_unwrap)%bin_number)].reshape(-1, bin_number), axis=1)
	third = int(len(a_data["a_roll"].values)/3)
	#heading= np.mean(heading_unwrap.tolist()[2*third:])
	heading= np.mean(a_data["a_heading"].tolist()[2*third:])
	roll= np.mean(a_data["a_roll"].tolist()[2*third:])
	pitch= np.mean(a_data["a_pitch"].tolist()[2*third:-1])
	heading_array.append(float(heading))
	roll_array.append(float(roll))
	pitch_array.append(float(pitch))

print(np.mean([abs(x) for x in roll_array]))
print(roll_array)
print(heading_array)
print(np.mean(pitch_array))
#plt.savefig(out_directory+"adcp_"+deployment_name+'profile'+str(i)+".png")
#plt.close()
plt.subplot(311);
plt.plot(roll_array)

plt.subplot(312)
plt.plot(heading_array)
plt.subplot(313)
plt.plot(pitch_array)
plt.show()