import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp


directory = '../../Data/deployment_raw/';
outdir = '../../plots/Ri/N2/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(10):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	plt.subplot(111)
	#c_data.plot.scatter('c_sal','c_pres','2illed');
	CT = gsw.CT_from_t(c_data['c_sal'].tolist(),c_data['c_temp'].tolist(),c_data['c_pres'].tolist())
	SA = gsw.SA_from_SP(c_data['c_sal'].tolist(),c_data['c_pres'].tolist(),174,-43)
	pressure = c_data['c_pres'].tolist()
	

	[N2,p_mid] = gsw.Nsquared(SA,CT,pressure)
	#get rid of any outliers
	meanN2 = np.mean(N2)
	stdN2 = np.std(N2)
	N2 = [x if (abs(x-meanN2)<=3*stdN2) else np.nan for x in N2]
	#interpolate over these outliers
	N2 = pd.Series(N2)
	N2 = N2.interpolate()
	N2 = N2.tolist()
	N2 = sp.savgol_filter(N2, 51, 3)
	#N2 = sp.spline_filter(N2)
	plt.plot(N2,p_mid)
	# N2 = N2*1000
	# N2 = np.array(N2)
	# N2[np.logical_and(N2 > -1E-5, N2<1E6)] 
	# middle = np.mean(N2)
	# print(N2)
	# sdd = np.std(N2)
	# print(sdd)

	plt.title('Buoyancy Frequency');
	plt.xlabel('N2');
	plt.ylabel('Pressure (dbar)');

	plt.suptitle("Profile "+ str(i))
	plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	plt.clf()
	#plt.show()

