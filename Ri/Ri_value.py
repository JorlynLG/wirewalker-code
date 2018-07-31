import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt
from beam2ENU import beam2ENU
from smooth import smooth

directory = '../../Data/deployment_raw/';
outdir = '../../plots/Ri/N2/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'
pd.set_option('display.max_colwidth', -1)


for i in range(4,5):
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
	time = a_data["a_time"].values[:-(len(a_data["a_time"].values)%bin_number)].reshape(-1, bin_number)
	a_time = [dt.datetime.strptime(x[:-10],"%Y-%m-%dT%H:%M:%S") for x in time[:,int(bin_number/2)]]
	#time = pd.to_datetime(time[:,int(bin_number/2)])
	start_index = c_time.index(a_time[1])
	end_index = c_time.index(a_time[-1])
	c_time = c_time[start_index-1:end_index+1]
	c_pres = c_data["c_pres"].tolist()[start_index-1:end_index+1]
	c_temp = c_data["c_temp"].tolist()[start_index-1:end_index+1]
	c_sal = c_data["c_sal"].tolist()[start_index-1:end_index+1]

 	#Generate the bouyancy frequency plot
	CT = gsw.CT_from_t(c_sal,c_temp,c_pres)
	SA = gsw.SA_from_SP(c_sal,c_pres,174,-43)	
	[N2,p_mid] = gsw.Nsquared(SA,CT,c_pres)
	#Generate the east, north and up
	[east,north,up] = beam2ENU([a_data["a_beam1"][0],a_data["a_beam2"][0],a_data["a_beam3"][0],a_data["a_beam4"][0]],a_data['a_heading'].values,a_data['a_pitch'].values,a_data['a_roll'].values,a_data['a_vel1'].values,a_data['a_vel2'].values,a_data['a_vel3'].values)	
	
	#Make sure everything is the same size
	bin_number = 10
	east = np.array(east)
	north = np.array(north)
	bin_east= np.mean(east[:-(len(east)%bin_number)].reshape(-1, bin_number), axis=1)
	bin_north= np.mean(north[:-(len(north)%bin_number)].reshape(-1, bin_number), axis=1)
	N2 = np.append(N2,N2[-1])

	#get rid of any outliers (dp,N2,bin_east,bin_north)
	N2 = pd.Series(N2)
	#N2[~((N2-N2.mean()).abs() > 3*N2.std())]
	N2 = np.where(((N2-N2.mean()).abs() > 3*N2.std()), np.nan, N2)
	N2 = pd.Series(N2).interpolate().rolling(20).mean()
	#N2 = N2.sort_values()
	
	#Shear magnitude values
	shallow = (slice(None, -1, None),)
	deep = (slice(1, None, None),)

	c_pres = np.array(c_pres)
	dp = c_pres[deep] - c_pres[shallow]
	
	dp = pd.Series(dp).rolling(20).mean()
	dp = [dp[x] if dp[x]!=0 else (dp[x+1]+dp[x-1])/2 for x in range(len(dp))]	
	dV = bin_east[deep]-bin_east[shallow]
	dV = pd.Series(dV)
	dV = np.where(((dV-dV.mean()).abs() > 3*dV.std()), np.nan, dV)
	dV = pd.Series(dV).interpolate().rolling(20).mean()	
	dU = bin_north[deep]-bin_north[shallow]
	dU = pd.Series(dU)
	dU = np.where(((dU-dU.mean()).abs() > 3*dU.std()), np.nan, dU)
	dU = pd.Series(dU).interpolate().rolling(20).mean()	
	
	#Shear Magnitude
	S2 = [((dU[x]/dp[x])**2) for x in range(len(dV))]
	S2 = pd.Series(S2).dropna()
	S2 = np.where(((S2-S2.mean()).abs() > 3*S2.std()), np.nan, S2)
	S2 = pd.Series(dU).interpolate().rolling(20).mean()	

	Ri = N2/S2
	#Ri.replace([np.inf,-np.inf], np.nan)
	Ri = pd.Series(Ri).interpolate().dropna()
	
	Ri = np.where(((Ri-Ri.mean()).abs() > Ri.std()), np.nan, Ri)
	Ri = pd.Series(Ri).interpolate().rolling(20).mean()	
	
	plt.plot(Ri)
	plt.show()


	# meanN2 = np.mean(N2)
	# stdN2 = np.std(N2)
	# N2 = [x if (abs(x-meanN2)<=3*stdN2) else np.nan for x in N2]
	# #interpolate over these outliers
	# N2 = pd.Series(N2)
	# N2 = N2.interpolate()
	# N2 = N2.tolist()
	# N2 = sp.savgol_filter(N2, 51, 3)


	# # plt.plot(N2,p_mid)
	# # plt.show()

	# shallow = (slice(None, -1, None),)
	# deep = (slice(1, None, None),)

	# db_to_pa = 1e4

	# [east,north,up] = beam2ENU([a_data["a_beam1"][0],a_data["a_beam2"][0],a_data["a_beam3"][0],a_data["a_beam4"][0]],a_data['a_heading'].values,a_data['a_pitch'].values,a_data['a_roll'].values,a_data['a_vel1'].values,a_data['a_vel2'].values,a_data['a_vel3'].values)	
	
	# bin_number = 10
	# east = np.array(east)
	# north = np.array(north)
	# bin_east= np.mean(east[:-(len(east)%bin_number)].reshape(-1, bin_number), axis=1)
	# bin_north= np.mean(north[:-(len(north)%bin_number)].reshape(-1, bin_number), axis=1)
	# print(len(bin_north))
	# print(len(dp))
	# #S2 = sp.savgol_filter(S2, 51, 3)

	# # bin_north = smooth(bin_north,50)
	# # bin_east = smooth(bin_east)

	# # dp = smooth(dp)
	# # dV = bin_east[deep]-bin_east[shallow]
	# # dV = smooth(dV)

	# # dU = bin_north[deep]-bin_north[shallow]
	# # dU = smooth(dU)
	# # S2 = [((dU[x]/dp[x])**2) for x in range(0,len(dV)-50)]
	# # S2 = [0.5*(S2[x-1]+S2[x+1]) if S2[x]==np.inf else S2[x] for x in range(len(S2))]
	# # S2 = [np.nanmean(S2) if np.isnan(S2[x]) else S2[x] for x in range(len(S2))]
	# # meanS2 = np.mean(S2[1:])
	# # stdS2 = np.std(S2[1:])
	# # print(meanS2)
	# # print(stdS2)
	# # S2 = [x if x<0.005 else np.nan for x in S2]
	# # #interpolate over these outliers
	# # S2 = pd.Series(S2)
	# # S2 = S2.interpolate()
	# # S2 = S2.tolist()
	# # plt.plot(S2)
	# # plt.show()
	# # #S2 = sp.savgol_filter(S2, 51, 3)

	# # Ri = N2/S2
