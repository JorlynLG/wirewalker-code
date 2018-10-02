import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from pytides.tide import Tide
import numpy as np


a_headers = ["date","time","height"]
a_dtypes = {"date":'str', "time":'str',"height":'float'}
k_tides = pd.read_csv('../../Data/tides/Kaikoura_tides.txt',sep="\t",header = 1,names=a_headers, dtype=a_dtypes)
k_tides['date_time'] = [datetime.strptime(k_tides["date"][x] + " "+k_tides["time"][x], "%Y-%m-%d %H:%M") for x in range(len(k_tides['date']))]
#print(f)
# for i, line in enumerate(f):

#     t.append(datetime.strptime(" ".join(line.split()[:2]), "%Y-%m-%d %H:%M"))
#     heights.append(float(line.split()[2]))
# f.close()

#height = [-0.56,0.48,-0.52,0.6,-0.59,0.52,-0.55,0.62,-0.63,0.59,-0.59,0.64,-0.69,0.67,-0.64,0.67]
#date = ["6/8/2018","6/8/2018","6/8/2018","6/9/2018","6/9/2018","6/9/2018","6/9/2018","6/10/2018","6/10/2018","6/10/2018","6/10/2018","6/11/2018","6/11/2018","6/11/2018","6/11/2018","6/12/2018"]
#time = ["5:48","11:55","17:56","0:10","6:29","12:39","18:43","0:55","7:13","13:26","19:33","1:43","7:59","14:15","20:26","2:33"]
#date_time = [datetime.strptime(date[x] + " "+time[x], "%m/%d/%Y %H:%M") for x in range(len(date))]
prediction_t0 = datetime(2018,6,8)
hours = 0.1*np.arange(7 * 24 * 10)
times = Tide._times(prediction_t0, hours)

my_tide = Tide.decompose(k_tides['height'], k_tides['date_time'])
my_prediction = my_tide.at(times)

f = interp1d( k_tides['date_time'],k_tides['height'],kind='cubic')

plt.plot(times, my_prediction)
plt.plot(k_tides['date_time'],k_tides['height'])
plt.show()
#my_prediction = my_tide.at(times)

#print(my_tide)
#plt.plot(my_tide)
#plt.show()