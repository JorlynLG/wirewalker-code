import pandas as pd
import numpy as np

directory1 = '../../Data/accelerometer_profiles/'
directory2 = '../../Data/deployment_raw/';
out_directory = '../../Data/accelerometer_profiles/'
file_type = 'accelerometer_raw'
deployment_name = 'deploy2_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(10):
	accel_data = pd.read_pickle(directory1+'accelerometer_raw')
	e_file = 'E'+("%07d" % (i,))
	e_data = pd.read_pickle(directory2+deployment_name+file_type+e_file)
	start_time = pd.DatetimeIndex(e_data["e_time"])[0]
	end_time = pd.DatetimeIndex(e_data["e_time"])[-1]
	#accel_data.set_index('accel_time')
	#print accel_dataebetween_time(start_time.to_pydatetime(),end_time.to_pydatetime())
	#profile_accel_data = accel_data.loc[accel_data['accel_time'] > start_time]
	profile_accel_data = accel_data.loc[accel_data['accel_time'] > start_time]

	profile_accel_data = profile_accel_data.loc[profile_accel_data['accel_time'] < end_time]
	#print profile_accel_data["accel_time"]
	#print profile_accel_data
	profile_accel_data.to_pickle(out_directory+"accelerometer_"+deployment_name+'profile'+str(i))

