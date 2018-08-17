import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt
from beam2ENU import beam2ENU


def N2_function(profile):

	directory = '../../Data/deployment_raw/';
	outdir = '../../plots/Ri/N2/';
	deployment_name = 'deploy1_';
	measurement_type = 'ctd_';
	file_type = 'raw_'

	filt_val = 20;

	c_file = 'C'+("%07d" % (profile,))
	a_file = 'A'+("%07d" % (profile,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)

	#Create time for CTD data
	start_time = a_data["a_time"].values[1][:-10]
	start_time = dt.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
	start_time = start_time - dt.timedelta(seconds=15)
	#c_time = np.arange(start_time, start_time+dt.timedelta(seconds=len(c_data["c_temp"].values)), dt.timedelta(seconds=1))
	c_time = [start_time+dt.timedelta(seconds=x) for x in range(len(c_data["c_temp"].values))]
	#Select only data points within a certain range of dbar

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
	data = pd.DataFrame({'time':c_time[start_index-1:end_index+1]})
	data['c_pres'] = pd.Series(c_data["c_pres"][start_index-1:end_index+1])
	data['c_temp'] = pd.Series(c_data["c_temp"][start_index-1:end_index+1])
	data['c_sal'] = pd.Series(c_data["c_sal"][start_index-1:end_index+1])

	data_start = data.index[data["c_pres"]>10][0]
	data_end = data.index[data["c_pres"]>100][0]

	data = data[data_start:data_end]
	#Create my panda dataframe
	#Ri_calcs = pd.DataFrame({'time':c_time})

	#Generate the bouyancy frequency plot
	CT = gsw.CT_from_t(data['c_sal'],data['c_temp'],data['c_pres'])
	SA = gsw.SA_from_SP(data['c_sal'],data['c_pres'],174,-43)	
	[N2,p_mid,dp] = gsw.Nsquared(SA,CT,data['c_pres'])
	Ri_calcs = pd.DataFrame({'pres':p_mid})
	Ri_calcs['dp'] = pd.Series(dp, index=Ri_calcs.index)
	#Ri_calcs['pres'] = pd.Series()
	Ri_calcs['N2'] = pd.Series(N2, index=Ri_calcs.index)
	Ri_calcs['N2'] = Ri_calcs['N2'].mask(((Ri_calcs['N2']-Ri_calcs['N2'].mean()).abs() > 2*Ri_calcs['N2'].std()))
	Ri_calcs['N2'] = Ri_calcs['N2'].interpolate()





	#Generate the east, north and up
	[east,north,up] = beam2ENU([a_data["a_beam1"][0],a_data["a_beam2"][0],a_data["a_beam3"][0],a_data["a_beam4"][0]],a_data['a_heading'].values,a_data['a_pitch'].values,a_data['a_roll'].values,a_data['a_vel1'].values,a_data['a_vel2'].values,a_data['a_vel3'].values)	
	
	#Make sure everything is the same size
	bin_number = 10
	east = np.array(east)
	north = np.array(north)
	if len(a_data["a_time"].values)%bin_number == 0:
		bin_east= np.mean(east.reshape(-1, bin_number), axis=1)
		bin_north= np.mean(north.reshape(-1, bin_number), axis=1)
	else:
		bin_east= np.mean(east[:-(len(east)%bin_number)].reshape(-1, bin_number), axis=1)
		bin_north= np.mean(north[:-(len(north)%bin_number)].reshape(-1, bin_number), axis=1)
	

	#get rid of any outliers (dp,N2,bin_east,bin_north)
	Ri_calcs['N2'] = Ri_calcs['N2'].mask(((Ri_calcs['N2']-Ri_calcs['N2'].mean()).abs() > 3*Ri_calcs['N2'].std()))
	Ri_calcs['N2'] = Ri_calcs['N2'].interpolate().rolling(filt_val).mean().abs()
	#N2 = N2.sort_values()

	#Shear magnitude values
	shallow = (slice(None, -1, None),)
	deep = (slice(1, None, None),)

	# c_pres = Ri_calcs['pres']
	# dp = c_pres[deep] - c_pres[shallow]
	# dp = [dp[x] if dp[x]!=0 else (dp[x+1]+dp[x-1])/2 for x in range(len(dp))]	
	# Ri_calcs['dp'] = pd.Series(dp, index=Ri_calcs.index)
	#Ri_calcs['dp'] = Ri_calcs['dp'].mask(Ri_calcs['dp'] == 0)
	#dp = [dp[x] if dp[x]!=0 else (dp[x+1]+dp[x-1])/2 for x in range(len(dp))]	

	Ri_calcs['dp'] = Ri_calcs['dp'].mask(((Ri_calcs['dp']-Ri_calcs['dp'].mean()).abs() > 3*Ri_calcs['dp'].std()))
	Ri_calcs['dp'] = Ri_calcs['dp'].interpolate().rolling(filt_val).mean()	
	


	bin_east = bin_east[data_start:data_end]
	bin_north = bin_north[data_start:data_end]
	dV = bin_east[deep]-bin_east[shallow]
	Ri_calcs['dV'] = pd.Series(dV, index=Ri_calcs.index)
	Ri_calcs['dV'] = Ri_calcs['dV'].mask(((Ri_calcs['dV']-Ri_calcs['dV'].mean()).abs() > 3*Ri_calcs['dV'].std()))
	Ri_calcs['dV'] = Ri_calcs['dV'].interpolate().rolling(filt_val).mean()

	dU = bin_north[deep]-bin_north[shallow]
	Ri_calcs['dU'] = pd.Series(dU, index=Ri_calcs.index)
	Ri_calcs['dU'] = Ri_calcs['dU'].mask(((Ri_calcs['dU']-Ri_calcs['dU'].mean()).abs() > 3*Ri_calcs['dU'].std()))
	Ri_calcs['dU'] = Ri_calcs['dU'].interpolate().rolling(filt_val).mean()	
	
	#Shear Magnitude
	Ri_calcs['S2'] = (Ri_calcs['dU']/Ri_calcs['dp'])**2 + (Ri_calcs['dV']/Ri_calcs['dp'])**2
	#S2 = [((Ri_calcs['dU'].values[x]/Ri_calcs['dp'][x])**2+(Ri_calcs['dV'][x]/Ri_calcs['dp'][x])**2)for x in range(len(dV))]
	#Ri_calcs['S2'] = Ri_calcs['S2'].mask(Ri_calcs['S2']> 100)	
	Ri_calcs['S2'] = Ri_calcs['S2'].mask(((Ri_calcs['S2']-Ri_calcs['S2'].mean()).abs() > Ri_calcs['S2'].std()))
	#Ri_calcs['S2'] = Ri_calcs['S2'].interpolate().rolling(filt_val).mean()
	Ri_calcs['S2'] = Ri_calcs['S2'].interpolate().abs()

	plt.plot(Ri_calcs['S2'])
	plt.savefig(outdir+'S2_'+str(profile)+".png")
	plt.clf()
	Ri_calcs['Ri'] = Ri_calcs['N2']/Ri_calcs['S2']
	Ri_calcs['Ri'] = Ri_calcs['Ri'].mask(((Ri_calcs['Ri']-Ri_calcs['Ri'].mean()).abs() > 3*Ri_calcs['Ri'].std()))
	Ri_calcs['Ri'] = Ri_calcs['Ri'].interpolate()	
	
	Ri_calcs['pres_round'] = Ri_calcs['pres'].round(0)
	binned = Ri_calcs.groupby(Ri_calcs['pres_round']).mean()
	binned = binned.rolling(10).mean()

	return binned