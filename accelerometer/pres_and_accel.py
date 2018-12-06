import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/accelerometer_profiles/'
directory1 = '../../Data/accelerometer_profiles/'
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(0,2,2):
    # pres_data = pd.read_pickle(directory+"accelerometer_pres_"+deployment_name+'profile'+str(i))
    # accel_data = pd.read_pickle(directory+"accelerometer_"+deployment_name+'profile'+str(i))
    # accel_data['y_accel'] = accel_data['y_accel'].interpolate().rolling(20).mean()    
    # pres_data['pres'] = pres_data['pres'].interpolate().rolling(20).mean()    
    # pres_data['dpres'] = np.append(np.diff(pres_data['pres']), np.diff(pres_data['pres'])[-1])
    # pres_data['dpres'] = pres_data['dpres'].interpolate().rolling(20).mean()    
    # pres_data['ddpres'] = np.append(np.diff(pres_data['dpres']),np.diff(pres_data['dpres'])[-1])
    # pres_data['ddpres'] = pres_data['ddpres'].interpolate().rolling(20).mean()    
        
    # #set the subplot configuration
    # #plt.plot(np.diff(pres_data["pres"]))
    # #plt.plot(np.diff(np.diff(pres_data["pres"])))
    # #print(len(np.diff(np.diff(pres_data["pres"]))))
    # #print(len(np.diff(pres_data["pres"])))
    # plt.plot(pres_data["ddpres"][0:100],pres_data["dpres"][0:100])
    # #Save and close figure
    # plt.show()


    pres_data = pd.read_pickle(directory1+'accelerometer_pres_raw')
    pres_data['pres'] = pres_data['pres'].interpolate().rolling(50).mean()    
    pres_data['dpres'] = np.append(np.diff(pres_data['pres']), np.diff(pres_data['pres'])[-1])
    pres_data['dpres'] = pres_data['dpres'].interpolate().rolling(50).mean()    
    pres_data['ddpres'] = np.append(np.diff(pres_data['dpres']),np.diff(pres_data['dpres'])[-1])
    pres_data['ddpres'] = pres_data['ddpres'].interpolate().rolling(50).mean()    
        
    #set the subplot configuration
    #plt.plot(np.diff(pres_data["pres"]))
    #plt.plot(np.diff(np.diff(pres_data["pres"])))
    #print(len(np.diff(np.diff(pres_data["pres"]))))
    #print(len(np.diff(pres_data["pres"])))
    plt.scatter(pres_data["ddpres"][25000:50000],pres_data["dpres"][25000:50000],s=1)
    #plt.plot(pres_data['pres'][25000:27000])
    #Save and close figure
    plt.show()
