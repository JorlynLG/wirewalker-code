import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/accelerometer_profiles/'
out_directory = '../../Plots/accelerometer/basic/'
file_type = 'accelerometer_raw'
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

for i in range(58):
    accel_data = pd.read_pickle(directory+"accelerometer_"+deployment_name+'profile'+str(i))
    #set the subplot configuration
    fig, axes = plt.subplots(nrows=3, ncols=1)
    #X-plot
    ax1 = accel_data.plot(x="accel_time",y="x_accel",ax=axes[0],legend=False)
    ax1.set_ylabel('x-acceleration (g)')
    #Y-plot
    ax2 = accel_data.plot(x="accel_time",y="y_accel",ax=axes[1],legend=False)
    ax2.set_ylabel('y-acceleration (g)')
    #Z-plot
    ax3 = accel_data.plot(x="accel_time",y="z_accel",ax=axes[2],legend=False)
    ax3.set_ylabel('z-acceleration (g)')
    ax3.set_xlabel('time')
    fig.suptitle("Profile "+ str(i))
    
    #Save and close figure
    plt.savefig(out_directory+"accelerometer_"+deployment_name+'profile'+str(i)+".png")
    plt.close()