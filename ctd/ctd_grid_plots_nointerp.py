import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/time/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_grid_';
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

v_val=0.1
h_val=1
verts = list(zip([-h_val,h_val,h_val,-h_val],[-v_val,-v_val,v_val,v_val]))

ymin = -120
ymax = 0
plt.figure()
plt.scatter(profile_array,neg_pressure_array,c=temperature_array, s = 90,marker=(verts,0))
plt.title('Temperature (C)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

plt.figure()
plt.scatter(profile_array,neg_pressure_array,c=salinity_array, s = 90,marker=(verts,0))
plt.title('Salinity (pss)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))


# #Salinity plot
# ax1 = plt.subplot(212)
# fig1 = ax1.scatter(xi,yi,s=4,c=grid_salinity)
# ax1.set_title('Salinity (pss)')
# ax1.set_xlabel('Profile')
# ax1.set_ylabel('Pressure (dbar)')	
# ax1.xaxis.set_label_position('bottom') # this moves the label to the top
# ax1.xaxis.set_ticks_position('bottom')
# ax1.yaxis.set_visible(False) # This erases the y ticks
# plt.colorbar(fig1,ax=ax1)

# #Temperature plot
# ax2 = plt.subplot(211)
# fig2 = ax2.scatter(xi,yi,s=4,c=grid_temperature)
# ax2.set_title('Temperature (C)')
# ax2.set_xlabel('Profile')
# ax2.xaxis.set_label_position('bottom') # this moves the label to the top
# ax2.xaxis.set_ticks_position('bottom') # this moves the ticks to the top
# plt.colorbar(fig2,ax=ax2)
# #plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
plt.show()