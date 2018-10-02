import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/pressure/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(40,41):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	# Three-panel plot
	fig2, (ax2, ax3, ax4) = plt.subplots(1,3)
	# Temperature
	ax2.plot(-c_data['c_pres'].values[150:750])
	ax2.set_ylabel('Pressure (dbar)')
	ax2.set_title('Pressure (dbar)')
	#ax2.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
	ax2.xaxis.set_label_position('top') # this moves the label to the top
	ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax2.xaxis.set_visible(False) # This erases the y ticks
	# Salinity
	ax3.plot(np.sort(-c_data['c_pres'].values[150:750])[::-1])
	ax3.set_title('Pressure Sorted (dbar)')
	ax3.xaxis.set_label_position('top') # this moves the label to the top
	ax3.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax3.xaxis.set_visible(False) # This erases the y ticks
	# Fluorescence
	ax4.plot(np.argsort(-c_data['c_dens'].values[150:750]))
	ax4.set_title('Pressure Sorted Index')
	ax4.xaxis.set_label_position('top') # this moves the label to the top
	ax4.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax4.xaxis.set_visible(False) # This erases the y ticks
	ax4.set_ylabel('Index')

	# plt.subplot(131);
	# #c_data.plot.scatter('c_sal','c_pres','filled');
	# plt.scatter(c_data['c_sal'].values,-c_data['c_pres'].values)
	# plt.title('Salinity (pss)');
	# plt.xlabel('Salinity (pss)');
	# plt.ylabel('Pressure (dbar)');

	# plt.subplot(132);
	# plt.scatter(c_data['c_temp'].values,-c_data['c_pres'].values)
	# plt.title('Temperature (C)');
	# plt.xlabel('Temperature (C)');

	# plt.subplot(133);
	# plt.scatter(c_data['c_dens'].values,-c_data['c_pres'].values)
	# plt.title('Density (kg/m3)');
	# plt.xlabel('Density (kg/m3)');

	#plt.suptitle("Profile "+ str(i))
	plt.show()

	#savefig(gcf,[outdir,'/',measurement_type, deployment_name,'profile',num2str(stas(mm))])