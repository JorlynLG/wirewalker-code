import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import gsw


directory = '../../Data/deployment_raw/';
outdir = '../../plots/eng/All/';
deployment_name = 'deploy1_';
measurement_type = 'eng_';
file_type = 'raw_'
profile_array = [];
pressure_array = [];
curr_array = [];

for i in range(0,58,2):
	e_file = 'E'+("%07d" % (i,))
	e_data = pd.read_pickle(directory+deployment_name+file_type+e_file)
	e_data['e_depth'] = pd.Series(gsw.z_from_p(e_data["e_pres"].values,-43), index=e_data.index)	
	
	#e_data['e_turb'] = e_data['e_turb'].mask(e_data['e_turb'] > 1000)
	#e_data['e_turb'] = e_data['e_turb'].interpolate()

	pressure_array.extend(e_data["e_depth"].tolist())
	curr_array.extend(e_data["e_curr"].tolist())
	profile_array.extend([i]*len(e_data["e_curr"].tolist()))

#neg_pressure_array = [-x for x in pressure_array]
v_val=1
h_val=1
verts = list(zip([-h_val,h_val,h_val,-h_val],[-v_val,-v_val,v_val,v_val]))

ymin = -120
ymax = 0
plt.figure()
plt.scatter(profile_array,pressure_array,c=curr_array, s = 90,marker=(verts,0))
plt.title('Turbidity (mV)')
plt.xlabel('Profile')
plt.ylabel('Depth (m)')
plt.colorbar()
plt.ylim((ymin, ymax))

plt.show()