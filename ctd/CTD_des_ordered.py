import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/basic/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

# for i in range(1):
# 	c_file = 'C'+("%07d" % (i,))
# 	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
# 	print(len(c_data['c_dens'].values))
# 	plt.plot(c_data['c_dens'].values[0:800],c_data['c_depth'].values[0:800],'-r')
# 	plt.plot(np.sort(c_data['c_dens'].values[0:800]),c_data['c_depth'].values[0:800],'-b')
# 	plt.xlabel('Density (kg/m3)')
# 	plt.ylabel('Depth (m)')
# 	plt.legend(['Density profile','Sorted Density Profile'])
# 	plt.show()
# #savefig(gcf,[outdir,'/',measurement_type, deployment_name,'profile',num2str(stas(mm))])

for i in range(1):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
	c_data['c_dens'] = c_data['c_dens']-1000
	fig2, (ax2, ax4) = plt.subplots(1,2,sharey=True)
	print(len(c_data['c_dens'].values))
	ax2.plot(c_data['c_dens'].values[0:800],c_data['c_depth'].values[0:800],'-r', linewidth =2)
	ax2.plot(np.sort(c_data['c_dens'].values[0:800]),c_data['c_depth'].values[0:800],'-b')
	ax2.set_xlabel('Density (kg/m3)')
	ax2.set_ylabel('Depth (m)')
	ax2.legend(['Density profile','Sorted Density Profile'])
	
	ax4.plot(np.argsort(c_data['c_dens'].values[0:800]),c_data['c_depth'].values[0:800],'-r')
	ax4.set_xlabel('Index')
	plt.show()
#savefig(gcf,[outdir,'/',measurement_type, deployment_name,'profile',num2str(stas(mm))])


