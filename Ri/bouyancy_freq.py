import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt


directory = '../../Data/deployment_raw/';
outdir = '../../plots/Ri/N2/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

filt_val = 20;

for i in range(0,2,2):
	c_file = 'C'+("%07d" % (i,))
	a_file = 'A'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)

	#Create time for CTD data
	start_time = a_data["a_time"].values[1][:-10]
	start_time = dt.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
	start_time = start_time - dt.timedelta(seconds=15)
	#c_time = np.arange(start_time, start_time+dt.timedelta(seconds=len(c_data["c_temp"].values)), dt.timedelta(seconds=1))
	c_time = [start_time+dt.timedelta(seconds=x) for x in range(len(c_data["c_temp"].values))]
 	

	bin_number = 10;
	if len(a_data["a_time"].values)%bin_number == 0:
		time = a_data["a_time"].values.reshape(-1, bin_number)
	else:
		time = a_data["a_time"].values[:-(len(a_data["a_time"].values)%bin_number)].reshape(-1, bin_number)
	#a_time = [dt.datetime.strptime(x[:-10],"%Y-%m-%dT%H:%M:%S") for x in time[:,int(bin_number/2)]]
	a_time = [dt.datetime.strptime(x[:-10],"%Y-%m-%dT%H:%M:%S") for x in time[:,int(bin_number/2)]]
	#time = pd.to_datetime(time[:,int(bin_number/2)])
	start_index = c_time.index(a_time[1])
	end_index = c_time.index(a_time[-1])
	c_time = c_time[start_index-1:end_index]
	c_pres = c_data["c_pres"].tolist()[start_index-1:end_index+1]
	c_temp = c_data["c_temp"].tolist()[start_index-1:end_index+1]
	c_sal = c_data["c_sal"].tolist()[start_index-1:end_index+1]

	#Create my panda dataframe
	Ri_calcs = pd.DataFrame({'time':c_time})
	
 	#Generate the bouyancy frequency plot

	CT = gsw.CT_from_t(c_sal,c_temp,c_pres)
	SA = gsw.SA_from_SP(c_sal,c_pres,174,-43)	
	[N2,p_mid] = gsw.Nsquared(SA,CT,c_pres)
	Ri_calcs['pres'] = pd.Series(p_mid)
	Ri_calcs['N2'] = pd.Series(N2, index=Ri_calcs.index)
	Ri_calcs['N2'] = Ri_calcs['N2'].mask(((Ri_calcs['N2']-Ri_calcs['N2'].mean()).abs() > 3*Ri_calcs['N2'].std()))
	Ri_calcs['N2'] = Ri_calcs['N2'].interpolate().rolling(10).mean()
	#Ri_calcs['pres'] = Ri_calcs['pres'].round(0)
	#binned = Ri_calcs['N2'].groupby(Ri_calcs['pres']).mean()

	#N2 = Ri_calcs['N2'].sort_values()

	#plt.plot(binned)
	#print(Ri_calcs)
	plt.plot(Ri_calcs['N2'],Ri_calcs['pres']*-1)
	#plt.show()	
	plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	plt.clf()
	#plt.show()
	#plt.plot(Ri)
	#plt.show()