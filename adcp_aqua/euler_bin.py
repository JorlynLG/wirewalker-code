import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_bins/';
deployment_name = 'deploy1_';
measurement_type = 'euler_';
file_type = 'raw_'
bin_number = 100

for i in range(2):
	a_file = 'A'+("%07d" % (i,))
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)
	
	#Datetime binning
	time = a_data["a_time"].values[:-(len(a_data["a_time"].values)%bin_number)].reshape(-1, bin_number)
	time = [dt.datetime.strptime(x[:-6],"%Y-%m-%dT%H:%M:%S.%f") for x in time[:,int(bin_number/2)]]
	#time = pd.to_datetime(time[:,int(bin_number/2)])

	#heading-plot
	plt.subplot(311);
	heading_unwrap = np.unwrap(a_data["a_heading"].apply(np.radians).values)
	bin_heading= np.mean(heading_unwrap[:-(len(heading_unwrap)%bin_number)].reshape(-1, bin_number), axis=1)
	plt.plot(time,np.degrees(bin_heading))
	#bin_heading= np.mean(a_data["a_heading"].values[:-(len(a_data["a_heading"].values)%bin_number)].reshape(-1, bin_number), axis=1)
	#plt.plot(time,bin_heading)
	plt.ylabel('heading (degree)')
	#roll-plot
	plt.subplot(312);
	bin_roll= np.mean(a_data["a_roll"].values[:-(len(a_data["a_roll"].values)%bin_number)].reshape(-1, bin_number), axis=1)
	plt.plot(time,bin_roll)
	plt.ylabel('roll (degree)')
	#pitch-plot
	plt.subplot(313);
	bin_pitch= np.mean(a_data["a_pitch"].values[:-(len(a_data["a_pitch"].values)%bin_number)].reshape(-1, bin_number), axis=1)
	plt.plot(time,bin_pitch)
	plt.ylabel('pitch (degree)')
	plt.xlabel('time')
	plt.suptitle("Profile "+ str(i))

	#Save and close figure
	plt.savefig(out_directory+"adcp_"+deployment_name+'profile'+str(i)+".png")
	plt.close()