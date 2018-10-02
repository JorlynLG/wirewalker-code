import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


directory = '../../Data/accelerometer_profiles/'
out_directory = '../../Plots/accelerometer/basic/'
file_type = 'accelerometer_raw'
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'
grid = pd.DataFrame(columns=['X_accel','y_accel','z_accel','pres','temp','profile']) # Note that there are now row data inserted.
for i in range(0,58,2):
    accel_data = pd.read_pickle(directory+"accelerometer_"+deployment_name+'profile'+str(i))
    pres_data = pd.read_pickle(directory+"accelerometer_pres_"+deployment_name+'profile'+str(i))
    #print(type(accel_data["accel_time"].tolist()(1)))

    #start_time = accel_data["accel_time"].tolist()
    #print(start_time)
    #start_time = dt.datetime.strptime(str(start_time),"%Y-%m-%dT%H:%M:%S")
    #accel_data["accel_time"] = [start_time for x in range(len(start_time))]
    accel_data.index = pd.DatetimeIndex(accel_data['accel_time'])
    pres_data.index = pd.DatetimeIndex(pres_data['pres_time'])
    accel_data = accel_data.resample('S').mean()
    data = pd.concat([accel_data, pres_data], axis=1, sort=False)
    data['pres'] = data['pres']*-1
    data['pres'] = data['pres'].round(-2)
    data = data.groupby(data['pres']).mean()
    data['profile'] = [i]*len(data)

    grid = pd.concat([grid,data])


grid['pres'] = grid['pres']/100
v_val=0.3
h_val=1
verts = list(zip([-h_val,h_val,h_val,-h_val],[-v_val,-v_val,v_val,v_val]))

ymin = -100
ymax = -20
plt.figure()
plt.scatter(grid['profile'],grid['pres'],c=grid['x_accel'], s=90, marker=(verts,0))
plt.title('X-Acceleration (g)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

plt.figure()
plt.scatter(grid['profile'],grid['pres'],c=grid['y_accel'], s=90, marker=(verts,0))
plt.title('Y-Acceleration (g)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

plt.figure()
plt.scatter(grid['profile'],grid['pres'],c=grid['z_accel'], s=90, marker=(verts,0))
plt.title('Z-Acceleration (g)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

    #set the subplot configuration
#fig, axes = plt.subplots(nrows=3, ncols=1)
# grid['pres'] = grid['pres']/100
# ax1 = plt.subplot(131)
# fig1 = ax1.scatter(grid['profile'],grid['pres'],s=13,c=grid['x_accel'])
# ax1.set_title('X-Acceleration (g)')
# ax1.set_xlabel('Profile')
# ax1.set_ylabel('Depth (m)')   
# ax1.xaxis.set_label_position('bottom') # this moves the label to the top
# ax1.xaxis.set_ticks_position('bottom')
# plt.ylim([-110,-20])

# plt.colorbar(fig1,ax=ax1)

# ax2 = plt.subplot(132)
# fig2 = ax2.scatter(grid['profile'],grid['pres'],s=13,c=grid['y_accel'])
# ax2.set_title('Y-acceleration (g)')
# ax2.set_xlabel('Profile')
# ax2.xaxis.set_label_position('bottom') # this moves the label to the top
# ax2.xaxis.set_ticks_position('bottom') # this moves the ticks to the top
# ax2.yaxis.set_visible(False) # This erases the y ticks
# plt.ylim([-110,-20])

# plt.colorbar(fig2,ax=ax2)

# ax3 = plt.subplot(133)
# fig3 = ax3.scatter(grid['profile'],grid['pres'],s=13,c=grid['z_accel'])
# ax3.set_title('Z-acceleration (g)')
# ax3.set_xlabel('Profile')
# ax3.xaxis.set_label_position('bottom') # this moves the label to the top
# ax3.xaxis.set_ticks_position('bottom') # this moves the ticks to the top
# ax3.yaxis.set_visible(False) # This erases the y ticks
# plt.colorbar(fig3,ax=ax3)

#ax1.xlim([-20,-120])

plt.show()

    # fig, axes = plt.subplots(nrows=3, ncols=1)
    # #X-plot
    # ax1 = accel_data.plot(x="accel_time",y="x_accel",ax=axes[0],legend=False)
    # ax1.set_ylabel('x-acceleration (g)')
    # #Y-plot
    # ax2 = accel_data.plot(x="accel_time",y="y_accel",ax=axes[1],legend=False)
    # ax2.set_ylabel('y-acceleration (g)')
    # #Z-plot
    # ax3 = accel_data.plot(x="accel_time",y="z_accel",ax=axes[2],legend=False)
    # ax3.set_ylabel('z-acceleration (g)')
    # ax3.set_xlabel('time')
    # fig.suptitle("Profile "+ str(i))
    
    # #Save and close figure
    # plt.savefig(out_directory+"accelerometer_"+deployment_name+'profile'+str(i)+".png")
    # plt.close()