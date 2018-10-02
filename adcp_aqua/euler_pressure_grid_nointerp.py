import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt
from beam2ENU import beam2ENU
import seawater as sw
import oceans as oc
from scipy.interpolate import griddata
import matplotlib.cm as cm

    
directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_bins/';
deployment_name = 'deploy1_';
measurement_type = 'euler_';
file_type = 'raw_'
bin_number = 100

profile_array = [];
heading_array = [];
roll_array = [];
pitch_array = [];
pres_array = []

for i in range(0,57,2):
    c_file = 'C'+("%07d" % (i,))
    a_file = 'A'+("%07d" % (i,))
    #Open the CTD data file that has all data stored as pandas
    c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
    a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)

    #Join CTD and ADCP data together (add time to CTD data)
    start_time = a_data["a_time"].values[1][:-10]
    start_time = dt.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
    start_time = start_time - dt.timedelta(seconds=15)
    c_data["c_time"] = [start_time+dt.timedelta(seconds=x) for x in range(len(c_data["c_temp"].values))]
    c_data.index = pd.DatetimeIndex(c_data['c_time'])

    #And average ADCP to resample at 1Hz
    a_data.index = pd.DatetimeIndex(a_data['a_time'])
    a_data = a_data.resample('S').mean()
    #Combine both datasets into one dataset by time
    data = pd.concat([a_data, c_data], axis=1, sort=False).dropna(axis='rows')

    #heading_unwrap = np.unwrap(a_data["a_heading"].apply(np.radians).values)
    #bin_heading= np.mean(heading_unwrap[:-(len(heading_unwrap)%bin_number)].reshape(-1, bin_number), axis=1)
    #bin_heading= np.mean(data["a_heading"].values[:-(len(data["a_heading"].values)%bin_number)].reshape(-1, bin_number), axis=1)
    #bin_roll= np.mean(data["a_roll"].values[:-(len(data["a_roll"].values)%bin_number)].reshape(-1, bin_number), axis=1)
    #bin_pitch= np.mean(data["a_pitch"].values[:-(len(data["a_pitch"].values)%bin_number)].reshape(-1, bin_number), axis=1)
    #bin_pres = np.mean(data["c_pres"].values[:-(len(data["c_pres"].values)%bin_number)].reshape(-1, bin_number), axis=1)
    # heading_array.extend(bin_heading.tolist())
    # roll_array.extend(bin_roll.tolist())
    # pitch_array.extend(bin_pitch.tolist())
    # profile_array.extend([i]*len(bin_pitch.tolist()))
    # time_array.extend(bin_pres.tolist())
    data['c_depth'] = data['c_depth'].round(0)
    data = data.groupby(data['c_depth']).mean()
    #data['c_depth'] = data['c_depth']

#    data['c_pres'] = data['c_pres'].round(0)
#    data = data.groupby(data['c_pres']).mean()

    heading_array.extend(data['a_heading'].tolist())
    roll_array.extend(data['a_roll'].tolist())
    pitch_array.extend(data['a_pitch'].tolist())
    profile_array.extend([i]*len(data['a_heading'].tolist()))
    #profile_array.extend(data.index.tolist())
    pres_array.extend(data.index.tolist())
    #pres_array.extend(data["c_depth"].tolist())

#neg_pressure_array = [-x for x in time_array]

#xi,yi = np.meshgrid(np.arange(0,58,1),np.arange(-110,-10,.25))
#grid_heading = griddata((profile_array,neg_pressure_array),heading_array,(xi,yi),method='linear')
#grid_pitch = griddata((profile_array,neg_pressure_array),pitch_array,(xi,yi),method='linear')
#grid_roll = griddata((profile_array,neg_pressure_array),roll_array,(xi,yi),method='linear')

v_val=0.2
h_val=1
verts = list(zip([-h_val,h_val,h_val,-h_val],[-v_val,-v_val,v_val,v_val]))

#plt.subplot(131)
ymin = -100
ymax = 0
plt.figure()
plt.scatter(profile_array,pres_array,c=heading_array, s = 90,marker=(verts,0))
plt.title('Heading (degrees)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

plt.figure()
plt.scatter(profile_array,pres_array,c=pitch_array, s = 90,marker=(verts,0))
plt.title('Pitch (degrees)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))


plt.figure()
plt.scatter(profile_array,pres_array,c=roll_array, s = 90,marker=(verts,0))
plt.title('Roll (degrees)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

# plt.subplot(132)
# plt.scatter(profile_array,neg_pressure_array,s=5,c=pitch_array)
# #plt.scatter(xi,yi,s=3,c=grid_pitch)
# plt.title('pitch (degrees)')
# plt.xlabel('Profile')
# plt.tick_params(
#     axis='y',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     left=False,      # ticks along the bottom edge are off
#     right=False,         # ticks along the top edge are off
#     labelleft=False) # labels along the bottom edge are off
# plt.colorbar()

# plt.subplot(133)
# plt.scatter(profile_array,neg_pressure_array,s=5,c=roll_array)
# #plt.scatter(xi,yi,s=3,c=grid_roll)
# plt.title('roll (degrees)')
# plt.xlabel('Profile')
# plt.tick_params(
#     axis='y',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     left=False,      # ticks along the bottom edge are off
#     right=False,         # ticks along the top edge are off
#     labelleft=False) # labels along the bottom edge are off
# plt.colorbar()  

#Save and close figure
plt.show()
#plt.savefig(out_directory+"adcp_"+deployment_name+'profile'+str(i)+".png")
#plt.close()