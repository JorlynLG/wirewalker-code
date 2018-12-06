import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ocean_tools import TKED
import gsw

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/LT_D_R/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

i=10
c_file = 'C'+("%07d" % (i,))
c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
print(len(c_data['c_pres']))
#plt.show()
# Temperature
fig2, (ax2, ax4) = plt.subplots(1,2,sharey=True)
ax2.plot(-c_data['c_pres'].values[100:500],'-r')
ax2.plot(-np.sort(c_data['c_pres'].values[100:500]),'-b')

ax2.set_ylabel('Depth (m)')
#ax2.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
ax2.set_title('Pressure (dbar)')
ax2.xaxis.set_label_position('top') # this moves the label to the top
ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax2.xaxis.set_visible(False) # This erases the y ticks	
ax2.legend(['Pressure (dbar)','Pressure sorted (dbar)'])
# Fluorescence
ax4.plot(np.argsort(c_data['c_pres'].values[100:500]),-c_data['c_pres'].values[100:500],'-g')
ax4.set_title('Pressure Sorted Index')
ax4.xaxis.set_label_position('top') # this moves the label to the top
ax4.xaxis.set_ticks_position('top') # this moves the ticks to the top
ax4.yaxis.set_visible(False) # This erases the y ticks	
ax4.xaxis.set_visible(False) # This erases the y ticks	

plt.show()