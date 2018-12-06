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

for i in range(1):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	CT = gsw.CT_from_t(c_data['c_sal'],c_data['c_temp'],c_data['c_pres'])
	SA = gsw.SA_from_SP(c_data['c_sal'],c_data['c_pres'],174,-43)
	pdens = gsw.sigma0(SA, CT)
	c_data["pdens"] = pdens
	[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales(c_data["c_depth"].values*-1,c_data['pdens'].values,full_output=True)

	c_data["Td"] = Td
	c_data["Td"] = c_data["Td"].rolling(10).mean()
	c_data["Td"] = c_data["Td"]**2
	c_data["Td"] = c_data["Td"].rolling(10).mean()
	c_data["LT"] = np.sqrt(c_data["Td"])

	#plt.show()
	# Temperature
	plt.plot(c_data["LT"],c='k')
	plt.plot(LT,c='k')
	plt.show()