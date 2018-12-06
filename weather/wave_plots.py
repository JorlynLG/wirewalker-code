import pandas as pd
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('banks_Jun2018.csv')

data["Date"] = pd.to_datetime(data["Date"])
# data_kaikoura = data.loc[data['Agent'] == 4506]
# data_campbell = data.loc[data['Agent'] == 4424]
# #plt.plot(data['Date_NZST'],data[''])
# #print(datetime.datetime(2018,6,1))
# #start_kaikoura = data_kaikoura.index[data_kaikoura['Date_NZST'] == datetime.datetime(2018,6,1)]
# #end_kaikoura = data_kaikoura.index[data_kaikoura['Date_NZST'] == datetime.datetime(2018,6,20)]
# #start_campbell = data_campbell.index[data_campbell['Date_NZST'] == datetime.datetime(2018,6,1)]
# #end_campbell = data_campbell.index[data_campbell['Date_NZST'] == datetime.datetime(2018,6,20)]
start = data.index[data['Date'] >= datetime.datetime(2018,6,2,0,0,0)]
fin = data.index[data['Date'] >= datetime.datetime(2018,6,18,0,0,0)]
print(start)
print(fin)
start = 48
fin = 785
#print(data_kaikoura)
f, (ax1, ax2, ax3) = plt.subplots(3, 1)
ax1.plot(data['Date'].values[start:fin],data['Dir deg'].values[start:fin],color='k')
ax1.set_title('Wave Direction')
ax1.set_ylabel('degrees')
ax1.xaxis.set_visible(False)
ax2.plot(data['Date'].values[start:fin],data['Tm02 sec'].values[start:fin],color='k')
ax2.set_title('Mean Period')
ax2.set_ylabel('sec')
ax2.xaxis.set_visible(False)
ax3.plot(data['Date'].values[start:fin],data['Hm0 m'].values[start:fin],color='k')
ax3.set_title('Significant wave height')
ax3.set_ylabel('m')


# #plt.plot(data_kaikoura['Date_NZST'],data_kaikoura['Wd'])
plt.show()