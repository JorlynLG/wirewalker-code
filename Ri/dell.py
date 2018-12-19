import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw
import scipy.signal as sp
import datetime as dt
from beam2ENU import beam2ENU
import seawater as sw
import oceans as oc
from scipy.interpolate import griddata
from ocean_tools import TKED

directory = '../../Data/deployment_raw/';
outdir = '../../plots/Ri/Ri_profile/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'
grid = pd.DataFrame(columns=['N2','shr2','Ri']) # Note that there are now row data insert

def create_data(directory, c_file, a_file):
    #Open the CTD data file that has all data stored as pandas
    c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)
    a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)

    #Join CTD and ADCP data together (add time to CTD data)
    start_time = a_data["a_time"].values[1][:-10]
    start_time = dt.datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S")
    start_time = start_time - dt.timedelta(seconds=15)
    c_data["c_time"] = [start_time+dt.timedelta(seconds=x) for x in range(len(c_data["c_temp"].values))]
    c_data.index = pd.DatetimeIndex(c_data['c_time'])

    #And average ADCP to resample at 1Hz
    a_data.index = pd.DatetimeIndex(a_data['a_time'])
    a_data = a_data.resample('S').mean()
    #Combine both datasets into one dataset by time
    data = pd.concat([a_data, c_data], axis=1, sort=False).dropna(axis='rows')
    #data_start = data.index[data["c_pres"]>20][0]
    #data_end = data.index[data["c_pres"]>100][0]
    #data = data[data_start:data_end]
    return data

# def buoyancy_freq(data):
#     #Get buoyancy frequency
#     CT = gsw.CT_from_t(data['c_sal'],data['c_temp'],data['c_pres'])
#     SA = gsw.SA_from_SP(data['c_sal'],data['c_pres'],174,-43)
#     [N2,p_mid,dp] = gsw.Nsquared(SA,CT,data['c_pres'])
#     #[n2,q,p_ave] = sw.bfrq(data['c_sal'],data['c_temp'],data['c_pres'],-43)
#     #N2 = [item[0] for item in n2]
#     N2 = np.array(N2)
#     data['N2'] = np.append(N2,N2[-1])

#     #filter buoyancy frequency by removing outliers
#     data['N2'] = data["N2"].replace([np.inf, -np.inf], np.nan)
#     data['N2'] = data['N2'].mask(((data['N2']-data['N2'].mean()).abs() > data['N2'].std()))
#     data['N2'] = data['N2'].interpolate().rolling(10).mean().abs()
#     #data['N2'] = data['N2'].mask(((data['N2']-data['N2'].mean()).abs() > 3*data['N2'].std()))
#     #data['N2'] = data['N2'].interpolate()
#     #plt.plot(data['N2'])
#     #plt.show()
#     return data
def buoyancy_freq(data):
    #Get buoyancy frequency
    dp = np.diff(data['c_pres'].values,axis=0)
    data['dp'] = np.append(dp,dp[-1])
    data['dp'] = data['dp'].mask(((data['dp']-data['dp'].mean()).abs() > data['dp'].std()))
    data['dp'] = data['dp'].interpolate().rolling(5).mean()
    CT = gsw.CT_from_t(data['c_sal'],data['c_temp'],data['c_pres'])
    SA = gsw.SA_from_SP(data['c_sal'],data['c_pres'],174,-43)
    pdens = gsw.sigma0(SA, CT)
    data['pdens'] = pdens
    dpdens = np.diff(data['pdens'].values,axis=0)
    data['dpdens'] = np.append(dpdens,dpdens[-1])
    data['dpdens'] = data['dpdens'].mask(((data['dpdens']-data['dpdens'].mean()).abs() > data['dpdens'].std()))
    data['dpdens'] = data['dpdens'].interpolate().rolling(5).mean()    
    data['N2'] = (9.7963*data['dpdens'])/(data['pdens']*data['dp'])

    
    
    #filter buoyancy frequency by removing outliers
    #data['N2'] = data['N2'].mask(data['N2']< 0.000005)
    data['N2'] = data["N2"].replace([np.inf, -np.inf], np.nan)
    data['N2'] = data['N2'].mask(((data['N2']-data['N2'].mean()).abs() > data['N2'].std()))
    data['N2'] = data['N2'].interpolate().rolling(10).mean()
    #data['N2'] = data['N2'].mask(((data['N2']-data['N2'].mean()).abs() > 3*data['N2'].std()))
    #data['N2'] = data['N2'].interpolate()
    
    #Sorted
    data['pdens_sort'] = np.sort(pdens)
    dpdens_sort = np.diff(data['pdens_sort'].values,axis=0)
    data['dpdens_sort'] = np.append(dpdens_sort,dpdens_sort[-1])
    data['dpdens_sort'] = data['dpdens_sort'].mask(((data['dpdens_sort']-data['dpdens_sort'].mean()).abs() > data['dpdens_sort'].std()))
    data['dpdens_sort'] = data['dpdens_sort'].interpolate().rolling(5).mean()    
    data['N2_sort'] = (9.7963*data['dpdens_sort'])/(data['pdens_sort']*data['dp'])    
    
    return data

for profile in range(1):
    c_file = 'C'+("%07d" % (profile,))
    a_file = 'A'+("%07d" % (profile,))
    
    data = create_data(directory, c_file, a_file)
    data = buoyancy_freq(data)
    
#     #data binned by 1 meter
#     ttitle = "1 meter bins"
#     data['c_depth'] = data['c_depth'].round(0)
#     data = data.groupby(data['c_depth']).mean()
#     data['profile'] = [profile]*len(data)
    
    #data binned by other meter
    ttitle = "0.5 meter bins"
    #data['c_depth'] = data['c_depth']*0.5
    data['c_depth'] = data['c_depth'].round(0)
    data = data.groupby(data['c_depth']).mean()
    #data['c_depth'] = data['c_depth']/0.5
    data['profile'] = [profile]*len(data)
    
    #if profile not in [6,12,16,28,34,48,56]:
    #    grid = pd.concat([grid,data])
    if profile not in [48]:
        grid = pd.concat([grid,data])

[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales(data["c_depth"].values*-1,data['c_dens'].values,full_output=True)
data["Td"] = Td
data["Td"] = data["Td"].rolling(10).mean()
data["Td"] = data["Td"]**2
data["Td"] = data["Td"].rolling(10).mean()
data["LT"] = np.sqrt(data["Td"])

x=[0.3752,
    0.3436,
    0.3379,
    0.4117,
    0.3590,
    0.2762,
    0.2940,
    0.3160,
    0.2922,
    0.2472,
    0.1878,
    0.1785,
    0.2092,
    0.1983,
    0.1397,
    0.1151,
    0.0936,
    0.0964,
    0.1247,
    0.1402,
    0.1113,
    0.1377,
    0.1597,
    0.1840,
    0.1525,
    0.1464,
    0.1341,
    0.1308,
    0.1149,
    0.1089,
    0.1168,
    0.1010,
    0.1118,
    0.1164,
    0.1208,
    0.0985,
    0.0766,
    0.0646,
    0.0743,
    0.0969,
    0.0918,
    0.0880,
    0.0763,
    0.0733,
    0.0533,
    0.0478,
    0.0502,
    0.0579,
    0.0504,
    0.0394,
    0.0465,
    0.0531,
    0.0644,
    0.0791,
    0.0953,
    0.0771,
    0.0541,
    0.0422,
    0.0374,
    0.0318,
    0.0250,
    0.0228,
    0.0270,
    0.0422,
    0.0532,
    0.0540,
    0.0531,
    0.0491,
    0.0376,
    0.0248,
    0.0337,
    0.0631,
    0.0751,
    0.0630,
    0.0481,
    0.0462,
    0.0494,
    0.0612,
    0.0821,
    0.0981,
    0.1130,
    0.1192,
    0.1204,
    0.1141,
    0.1086,
    0.1166,
    0.1321,
    0.1469,
    0.1488,
    0.1450,
    0.1390,
    0.1404,
    0.1511,
    0.1718,
    0.1830,
    0.1682,
    0.1520,
    0.1522,
    0.1587,
    0.1627,
    0.1736,
    0.1904,
    0.1969,
    0.1976,
    0.1957,
    0.1933,
    0.1816,
    0.1755,
    0.1706,
    0.1671]
first = [i * 0.0001 for i in x]
press = [-10.6600,-11.6600,-12.6600,-13.6600,-14.6600,-15.6600,-16.6600,-17.6600,-18.6600,-19.6600,-20.6600,-21.6600,-22.6600,-23.6600,-24.6600,-25.6600,-26.6600,-27.6600,-28.6600,-29.6600,-30.6600,-31.6600,-32.6600,-33.6600,-34.6600,-35.6600,-36.6600,-37.6600,-38.6600,-39.6600,-40.6600,-41.660,-42.6600,-43.6600,-44.6600,-45.6600,-46.6600,-47.6600,-48.6600,-49.6600,-50.6600,-51.6600,-52.6600,-53.6600,-54.6600,-55.6600,-56.6600,-57.6600,-58.6600,-59.6600,-60.6600,-61.6600,-62.6600,-63.6600,-64.6600,-65.6600,-66.6600,-67.6600,-68.6600,-69.6600,-70.6600,-71.6600,-72.6600,-73.6600,-74.6600,-75.6600,-76.6600,-77.6600,-78.6600,-79.6600,-80.6600,-81.6600,-82.6600,-83.6600,-84.6600,-85.6600,-86.6600,-87.6600,-88.6600,-89.6600,-90.6600 ,-91.6600,-92.6600,-93.6600,-94.6600,-95.6600,-96.6600, -97.6600,-98.6600, -99.6600, -100.6600, -101.6600, -102.6600, -103.6600, -104.6600,-105.6600,-106.6600, -107.6600, -108.6600, -109.6600, -110.6600, -111.6600, -112.6600, -113.6600,-114.6600, -115.6600, -116.6600, -117.6600,-118.6600,-119.6600]

plt.semilogx((0.64*(data['LT'].values**2)*(data['N2_sort'].values**(3/2))),-data['c_pres'].values, 'k')
plt.xlabel("$\epsilon$ [W/kg]")
plt.ylabel("P (dbar)")
plt.scatter(first,press,color='k',s=2)
plt.xlim((0.000000001, 0.001))
plt.ylim((-85, -15))


#print(-data['c_pres'].values[5:-5])

plt.show()