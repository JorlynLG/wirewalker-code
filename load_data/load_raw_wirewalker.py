import pandas as pd
import numpy as np
import gsw
import matplotlib.pyplot as plt


directory = '../../Data/deployment2_unpacked/'
out_directory = '../../Data/deployment_raw/'
deployment = 'deploy2_'
file_type = 'raw_'


for i in range(1):
	#Files that we want to open and save from
	e_file = 'E'+("%07d" % (i,))
	a_file = 'A'+("%07d" % (i,))
	c_file = 'C'+("%07d" % (i,))
	
	#Read the text files from Wirewalker
	a_headers = ["a_time","sos","a_temp","a_pres","a_heading","a_pitch","a_roll","a_magx","a_magy","a_magz","a_beams","a_cells","a_beam1","a_beam2","a_beam3","a_beam4","a_beam5","a_vel1","a_vel2","a_vel3","a_amp1","a_amp2","a_amp3","a_corr1","a_corr2","a_corr3"]
	a_dtypes = {"a_time":'str', "sos":'float',"a_temp":'float',"a_pres":'float',"a_heading":'float',"a_pitch":'float',"a_roll":'float',"a_magx":'float',"a_magy":'float',"a_magz":'float',"a_beams":'float',"a_cells":'float',"a_beam1":'float',"a_beam2":'float',"a_beam3":'float',"a_beam4":'float',"a_beam5":'float',"a_vel1":'float',"a_vel2":'float',"a_vel3":'float',"a_amp1":'float',"a_amp2":'float',"a_amp3":'float',"a_corr1":'float',"a_corr2":'float',"a_corr3":'float'}
	a_parse_dates = ["a_time"]
	a_data = pd.read_csv(directory+a_file+'.txt', sep=",",header = 1,skipfooter=4,names=a_headers, dtype=a_dtypes, parse_dates=a_parse_dates)
		
	#Correlation of all the velocity beam data
	a_vel1 = a_data["a_vel1"].values
	a_vel2 = a_data["a_vel2"].values
	a_vel3 = a_data["a_vel3"].values

	meanV1 = np.mean(a_vel1)
	stdV1 = np.std(a_vel1)
	meanV2 = np.mean(a_vel2)
	stdV2 = np.std(a_vel2)
	meanV3 = np.mean(a_vel3)
	stdV3 = np.std(a_vel3)	

	for i in range(len(a_vel1)):
		if (a_data["a_corr1"].values[i]<75 or a_data["a_corr2"].values[i]<75 or a_data["a_corr3"].values[i]<75):
			a_vel1[i] = np.nan
			a_vel2[i] = np.nan
			a_vel3[i] = np.nan
	for i in range(len(a_vel1)):
		if (abs(a_vel1[i]-meanV1)>=3*stdV1):
			a_vel1[i] = np.nan
	for i in range(len(a_vel2)):
		if (abs(a_vel2[i]-meanV2)>=3*stdV2):
			a_vel2[i] = np.nan
	for i in range(len(a_vel3)):
		if (abs(a_vel3[i]-meanV3)>=3*stdV3):
			a_vel3[i] = np.nan

	a_vel1 = pd.Series(a_vel1, index=a_data.index)
	a_vel1 = a_vel1.interpolate()
	a_vel2 = pd.Series(a_vel2, index=a_data.index)
	a_vel2 = a_vel2.interpolate()
	a_vel3 = pd.Series(a_vel3, index=a_data.index)
	a_vel3 = a_vel3.interpolate()
	a_data['a_vel1'] = a_vel1
	a_data['a_vel2'] = a_vel2
	a_data['a_vel3'] = a_vel3

	a_data.to_pickle(out_directory+deployment+file_type+a_file)
	
	e_headers = ["e_time","e_curr","e_volt","e_pres","e_turb","e_gain","e_par","e_chl","e_bb","e_cdom"]
	e_dtypes = 	{"e_time":'str',"e_curr":'float',"e_volt":'float',"e_pres":'float',"e_turb":'float',"e_gain":'float',"e_par":'float',"e_chl":'float',"e_bb":'float',"e_cdom":'float'}
	e_parse_dates = ["e_time"]
	e_data = pd.read_csv(directory+e_file+'.txt',sep=",",header=3,skipfooter=5,names=e_headers, dtype=e_dtypes, parse_dates=e_parse_dates)
	e_data.to_pickle(out_directory+deployment+file_type+e_file)
	
	c_headers = ["c_cond","c_temp","c_pres","c_hz"]	
	c_data = pd.read_csv(directory+c_file+'.txt', sep=",",header = 1,skipfooter=4, names=c_headers)
	plt.plot(c_data['c_cond'])
	plt.show()
	plt.plot(c_data['c_temp'])
	plt.show()
	plt.plot(c_data['c_pres'])
	plt.show()	
	c_data['c_sal'] = pd.Series(gsw.SP_from_C(c_data["c_cond"].tolist(),c_data["c_temp"].tolist(),c_data["c_pres"].tolist()), index=c_data.index)
	plt.plot(c_data['c_sal'])
	plt.show()
	c_data['c_depth'] = pd.Series(gsw.z_from_p(c_data["c_pres"].values,-43), index=c_data.index)
	c_data['c_dens'] = pd.Series(gsw.rho(c_data["c_sal"].values,c_data["c_temp"].values,np.zeros(len(c_data["c_pres"].values))), index=c_data.index)
	c_data.to_pickle(out_directory+deployment+file_type+c_file)
	#print a_data
	#print [0]*len(c_data["c_pres"].values)