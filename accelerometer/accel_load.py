import pandas as pd
import numpy as np
import datetime

directory = '../../Data/accelerometer_raw/'
out_directory = '../../Data/accelerometer_profiles/'
file_type = 'accelerometer_raw'

a_headers = ["accel_date","accel_time","accel_mill","x_accel","y_accel","z_accel"]
a_dtypes = {"accel_date":'str',"accel_time":'str',"accel_mill":'str',"x_accel":'float',"y_accel":'float',"z_accel":'float'}
accel_data = pd.read_csv(directory+'Acc1806110238080001.csv', sep=",",names=a_headers,header=1, dtype=a_dtypes)
#split_time = accel_data["accel_date"].str.split(pat="/")
#split_time = accel_data["accel_date"].str.replace(pat="/",repl="-")
split_time = accel_data["accel_date"].tolist()
split_string = [x.split("/") for x in split_time]
date_string = [x[1]+'/'+x[2]+'/'+x[0] for x in split_string]
date_string = pd.Series(date_string, index=accel_data.index)

#print datetime.datetime.strptime(split_time[0], "%Y-%m-%d").strftime("%d/%m/%Y")
#accel_data["accel_time"] = pd.to_datetime(date_sting+' '+accel_data["accel_time"]+ '.'+accel_data["accel_mill"])
accel_data["accel_time"] = pd.to_datetime(date_string+' '+accel_data["accel_time"]+ '.'+accel_data["accel_mill"])


#print accel_data["accel_time"]
#zz=pd.DatetimeIndex(accel_data["accel_time"])
#print zz.month
accel_data.to_pickle(out_directory+file_type)
