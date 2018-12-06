import pandas as pd
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('KaikouraCampbell.csv')
data["Date_NZST"] = pd.to_datetime(data["Date_NZST"])
data_kaikoura = data.loc[data['Agent'] == 4506]
data_campbell = data.loc[data['Agent'] == 4424]
#plt.plot(data['Date_NZST'],data[''])
#print(datetime.datetime(2018,6,1))
start_kaikoura = data_kaikoura.index[data_kaikoura['Date_NZST'] >= datetime.datetime(2018,6,2,0,0,0)]
#end_kaikoura = data_kaikoura.index[data_kaikoura['Date_NZST'] == datetime.datetime(2018,6,18)]
#start_campbell = data_campbell.index[data_campbell['Date_NZST'] == datetime.datetime(2018,6,1)]
#end_campbell = data_campbell.index[data_campbell['Date_NZST'] == datetime.datetime(2018,6,20)]

print(start_kaikoura)
#print(data_kaikoura)
start_kaikoura = 768
end_kaikoura = 1152
start_campbell = 767
end_campbell = 1151

#print(data_kaikoura)
f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
ax1.plot(data_kaikoura['Date_NZST'].values[start_kaikoura:end_kaikoura],data_kaikoura['Wd'].values[start_kaikoura:end_kaikoura],color='k')
ax1.set_title('Wind Direction')
ax1.set_ylabel('degrees')
ax1.xaxis.set_visible(False)
#plt.plot(data_kaikoura['Date_NZST'].values[start_campbell:end_campbell],data_kaikoura['Wd'].values[start_campbell:end_campbell])
ax2.plot(data_kaikoura['Date_NZST'].values[start_kaikoura:end_kaikoura],data_kaikoura['Wsmps'].values[start_kaikoura:end_kaikoura],color='k')
ax2.set_title('Wind Speed')
ax2.set_ylabel('m/s')
ax2.xaxis.set_visible(False)
ax3.plot(data_kaikoura['Date_NZST'].values[start_kaikoura:end_kaikoura],data_kaikoura['Tmax'].values[start_kaikoura:end_kaikoura],color='k')
ax3.set_title('Average Temperature')
ax3.set_ylabel('celcius')
ax3.xaxis.set_visible(False)
ax4.plot(data_kaikoura['Date_NZST'].values[start_kaikoura:end_kaikoura],data_kaikoura['PresMSL'].values[start_kaikoura:end_kaikoura],color='k')
ax4.set_title('Pressure')
ax4.set_ylabel('mbar')


#plt.plot(data_kaikoura['Date_NZST'],data_kaikoura['Wd'])
plt.show()