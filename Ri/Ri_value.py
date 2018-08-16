import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt
from beam2ENU import beam2ENU
from smooth import smooth

directory = '../../Data/deployment_raw/';
outdir = '../../plots/Ri/Ri_profile/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'
pd.set_option('display.max_colwidth', -1)

filt_val = 20

for i in range(10):
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
	#N2 = np.append(N2,N2[-1])
	Ri_calcs['N2'] = pd.Series(N2, index=Ri_calcs.index)

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
	Ri_calcs['N2'] = Ri_calcs['N2'].interpolate().rolling(filt_val).mean()
	#N2 = N2.sort_values()

	#Shear magnitude values
	shallow = (slice(None, -1, None),)
	deep = (slice(1, None, None),)

	c_pres = np.array(c_pres)
	dp = c_pres[deep] - c_pres[shallow]
	dp = [dp[x] if dp[x]!=0 else (dp[x+1]+dp[x-1])/2 for x in range(len(dp))]	
	Ri_calcs['dp'] = pd.Series(dp, index=Ri_calcs.index)
	#Ri_calcs['dp'] = Ri_calcs['dp'].mask(Ri_calcs['dp'] == 0)
	#dp = [dp[x] if dp[x]!=0 else (dp[x+1]+dp[x-1])/2 for x in range(len(dp))]	
	Ri_calcs['dp'] = Ri_calcs['dp'].mask(((Ri_calcs['dp']-Ri_calcs['dp'].mean()).abs() > 3*Ri_calcs['dp'].std()))
	Ri_calcs['dp'] = Ri_calcs['dp'].interpolate().rolling(filt_val).mean()	

	dV = bin_east[deep]-bin_east[shallow]
	print()
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
	Ri_calcs['S2'] = Ri_calcs['S2'].interpolate().rolling(filt_val).mean()
	
	#S2 = np.where(((S2-S2.mean()).abs() > 3*S2.std()), np.nan, S2)
	#S2 = pd.Series(dU).interpolate().rolling(20).mean()	

	Ri_calcs['Ri'] = Ri_calcs['N2']/Ri_calcs['S2']
	Ri_calcs['Ri'] = Ri_calcs['Ri'].interpolate()
	Ri_calcs['Ri'] = Ri_calcs['Ri'].mask(((Ri_calcs['Ri']-Ri_calcs['Ri'].mean()).abs() > 3*Ri_calcs['Ri'].std()))
	Ri_calcs['Ri'] = Ri_calcs['Ri'].interpolate().rolling(filt_val).mean()	
	plt.plot(Ri_calcs['Ri'],Ri_calcs['pres']*-1)
	plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	plt.clf()
	#plt.show()
	#plt.plot(Ri)
	#plt.show()