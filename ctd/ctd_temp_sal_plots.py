import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/temp_sal/';
deployment_name = 'deploy2_';
measurement_type = 'ctd_T_S_';
profiles = ''
file_type = 'raw_'
fig = plt.figure()
ax1 = fig.add_subplot(111)

x=[]
y=[]
z=[]

for i in range(10):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	#plt.subplot(131);
	#c_data.plot.scatter('c_sal','c_pres','filled');
	x.extend(c_data['c_sal'].tolist())
	y.extend(c_data['c_temp'].tolist())
	z.extend(c_data['c_dens'].tolist())
	
# z[:] = [(i-1000)*1000 for i in z]

# xi,yi = np.meshgrid(np.arange(min(x), max(x), 0.001),np.arange(min(y), max(y), 0.001))
# grid_dens = griddata((x,y),z,(xi,yi),method='linear')
# CS = plt.contour(xi,yi,grid_dens)
# ax1.clabel(CS, fontsize=12, inline=1, fmt='%1.2f') # Label every second level
# plt.colorbar()
 
ax1.scatter(x,y, c='k',s=5)
plt.xlabel('Salinity (pss)');
plt.ylabel('Temperature (C)');
plt.title('T-S Diagram: '+ profiles)

#plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
#plt.clf()
plt.savefig(outdir+measurement_type+deployment_name+ profiles+".png")	
#plt.show()

#savefig(gcf,[outdir,'/',measurement_type, deployment_name,'profile',num2str(stas(mm))])