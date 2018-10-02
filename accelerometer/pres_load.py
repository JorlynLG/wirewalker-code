import pandas as pd
import numpy as np
import datetime

directory = '../../Data/accelerometer_raw/'
out_directory = '../../Data/accelerometer_profiles/'
file_type = 'accelerometer_pres_raw'

a_headers = ["pres_date","pres_time","pres_mill","d1","d2","pres","temp"]
a_dtypes = {"pres_date":'str',"pres_time":'str',"pres_mill":'str',"d1":'float',"d2":'float',"pres":'float',"temp":'float'}
pres_data = pd.read_csv(directory+'Press1806110238080001.csv', sep=",",names=a_headers,header=1, dtype=a_dtypes)
#split_time = accel_data["accel_date"].str.split(pat="/")
#split_time = accel_data["accel_date"].str.replace(pat="/",repl="-")
split_time = pres_data["pres_date"].tolist()
split_string = [x.split("/") for x in split_time]
date_string = [x[1]+'/'+x[2]+'/'+x[0] for x in split_string]
date_string = pd.Series(date_string, index=pres_data.index)

#print datetime.datetime.strptime(split_time[0], "%Y-%m-%d").strftime("%d/%m/%Y")
#accel_data["accel_time"] = pd.to_datetime(date_sting+' '+accel_data["accel_time"]+ '.'+accel_data["accel_mill"])
pres_data["pres_time"] = pd.to_datetime(date_string+' '+pres_data["pres_time"]+ '.'+pres_data["pres_mill"])


#print accel_data["accel_time"]
#zz=pd.DatetimeIndex(accel_data["accel_time"])
#print zz.month
pres_data.to_pickle(out_directory+file_type)
