from datetime import datetime
from pytides.tide import Tide
import numpy as np
import matplotlib.pyplot as plt


##Prepare our tide data
station_id = '8516945'

heights = []
t = []

f = open('data/'+station_id, 'r')
for i, line in enumerate(f):
    t.append(datetime.strptime(" ".join(line.split()[:2]), "%Y-%m-%d %H:%M"))
    heights.append(float(line.split()[2]))
f.close()

#For a quicker decomposition, we'll only use hourly readings rather than 6-minutely readings.
heights = np.array(heights[::10])
t = np.array(t[::10])

##Prepare a list of datetimes, each 6 minutes apart, for a week.
prediction_t0 = datetime(2013,1,1)
hours = 0.1*np.arange(7 * 24 * 10)
times = Tide._times(prediction_t0, hours)

##Fit the tidal data to the harmonic model using Pytides
my_tide = Tide.decompose(heights, t)
##Predict the tides using the Pytides model.
my_prediction = my_tide.at(times)

##Prepare NOAA's results
noaa_verified = []
noaa_predicted = []

f = open('data/'+station_id+'_noaa', 'r')
for line in f:
    noaa_verified.append(line.split()[2])
    noaa_predicted.append(line.split()[3])
f.close()

##Plot the results
plt.plot(hours, my_prediction, label="Pytides")
plt.plot(hours, noaa_predicted, label="NOAA Prediction")
plt.plot(hours, noaa_verified, label="NOAA Verified")
plt.legend()
plt.title('Comparison of Pytides and NOAA predictions for Station: ' + str(station_id))
plt.xlabel('Hours since ' + str(prediction_t0) + '(GMT)')
plt.ylabel('Metres')
plt.show()