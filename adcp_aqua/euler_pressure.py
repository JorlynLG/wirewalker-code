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
	time = a_data["a_time"].values[:-(len(a_data["a_time"].values)%bin_number)].reshape(-1, bin_number)
	time = [dt.datetime.strptime(x[:-6],"%Y-%m-%dT%H:%M:%S.%f") for x in time[:,int(bin_number/2)]]
	#time = [x.total_seconds() for x in time]

	#heading_unwrap = np.unwrap(a_data["a_heading"].apply(np.radians).values)
	#bin_heading= np.mean(heading_unwrap[:-(len(heading_unwrap)%bin_number)].reshape(-1, bin_number), axis=1)
	bin_heading= np.mean(a_data["a_heading"].values[:-(len(a_data["a_heading"].values)%bin_number)].reshape(-1, bin_number), axis=1)
	bin_roll= np.mean(a_data["a_roll"].values[:-(len(a_data["a_roll"].values)%bin_number)].reshape(-1, bin_number), axis=1)
	bin_pitch= np.mean(a_data["a_pitch"].values[:-(len(a_data["a_pitch"].values)%bin_number)].reshape(-1, bin_number), axis=1)
	heading_array.extend(bin_heading.tolist())
	roll_array.extend(bin_roll.tolist())
	pitch_array.extend(bin_pitch.tolist())
	profile_array.extend([i]*len(bin_pitch.tolist()))
	time_array.extend(range(len(time)))

plt.subplot(131)
plt.scatter(profile_array,time_array,s=9,c=heading_array)
plt.title('heading (degrees)')
plt.xlabel('Profile')
plt.ylabel('time')
plt.colorbar()

plt.subplot(132)
plt.scatter(profile_array,time_array,s=9,c=pitch_array)
plt.title('pitch (degrees)')
plt.xlabel('Profile')
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,      # ticks along the bottom edge are off
    right=False,         # ticks along the top edge are off
    labelleft=False) # labels along the bottom edge are off
plt.colorbar()

plt.subplot(133)
plt.scatter(profile_array,time_array,s=7,c=roll_array)
plt.title('roll (degrees)')
plt.xlabel('Profile')
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,      # ticks along the bottom edge are off
    right=False,         # ticks along the top edge are off
    labelleft=False) # labels along the bottom edge are off
plt.colorbar()	

#Save and close figure
plt.show()
#plt.savefig(out_directory+"adcp_"+deployment_name+'profile'+str(i)+".png")
#plt.close()