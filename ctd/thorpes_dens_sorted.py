import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ocean_tools import TKED
import gsw

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/LT_D_R/';
deployment_name = 'deploy2_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(10):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	CT = gsw.CT_from_t(c_data['c_sal'],c_data['c_temp'],c_data['c_pres'])
	SA = gsw.SA_from_SP(c_data['c_sal'],c_data['c_pres'],174,-43)
	pdens = gsw.sigma0(SA, CT)
	c_data["pdens"] = pdens
	[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales1(c_data["c_depth"].values*-1,c_data['pdens'].values,full_output=True)


	#plt.show()
	fig2, (ax2, ax3, ax4) = plt.subplots(1,3,sharey=True)
	# Temperature
	ax2.plot(c_data['pdens'],c_data["c_depth"].values,c='k')
	ax2.set_ylabel('Depth (m)')
	#ax2.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
	ax2.set_xlabel('Density (kg/m3)')
	ax2.xaxis.set_label_position('top') # this moves the label to the top
	ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
	# Salinity
	ax3.plot(LT,c_data["c_depth"].values,c='k')
	ax3.set_xlabel('LT (m)')
	ax3.xaxis.set_label_position('top') # this moves the label to the top
	ax3.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax3.yaxis.set_visible(False) # This erases the y ticks
	# Fluorescence
	ax4.plot(R,c_data["c_depth"].values,c='k')
	ax4.axvline(x=0.25, c='b')
	ax4.set_xlabel('Overturn (Ro)')
	ax4.xaxis.set_label_position('top') # this moves the label to the top
	ax4.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax4.yaxis.set_visible(False) # This erases the y ticks	

	plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	plt.clf()
c