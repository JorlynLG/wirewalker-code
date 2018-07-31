import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/basic/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(1):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	plt.subplot(131);
	#c_data.plot.scatter('c_sal','c_pres','filled');
	plt.scatter(c_data['c_sal'].values,-c_data['c_pres'].values)
	plt.title('Salinity (pss)');
	plt.xlabel('Salinity (pss)');
	plt.ylabel('Pressure (dbar)');

	plt.subplot(132);
	plt.scatter(c_data['c_temp'].values,-c_data['c_pres'].values)
	plt.title('Temperature (C)');
	plt.xlabel('Temperature (C)');

	plt.subplot(133);
	plt.scatter(c_data['c_dens'].values,-c_data['c_pres'].values)
	plt.title('Density (kg/m3)');
	plt.xlabel('Density (kg/m3)');

	plt.suptitle("Profile "+ str(i))
	plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	plt.clf()
#savefig(gcf,[outdir,'/',measurement_type, deployment_name,'profile',num2str(stas(mm))])