import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ocean_tools import TKED

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/Nsqu/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(58):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales1(c_data["c_pres"].values*-1,c_data['c_dens'].values,full_output=True)
	

	plt.plot(Nsqu,c_data["c_pres"].values*-1)
	plt.xlabel("Thorpe_scales (m)")
	plt.ylabel('pressure (dbar)')

	plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	plt.clf()
	#plt.show()