import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ocean_tools import TKED

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/thorpe/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

LT_array = []
depth_array = []
profile_array = []
grid = pd.DataFrame(columns=['LT','c_depth']) # Note that there are now row data inserted.for i in range(0,58,2):

for i in range(0,50,2):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales1(c_data["c_depth"].values*-1,c_data['c_dens'].values,full_output=True)
	
	c_data['LT'] = LT
	grid = pd.concat([grid,c_data])

	# plt.plot(LT,c_data["c_depth"].values)
	# plt.xlabel("Thorpe_scales (m)")
	# plt.ylabel('Depth (m)')

	# plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	# plt.clf()
	#plt.show()
grid['c_depth'] = grid['c_depth'].round(0)
grid = grid.groupby(grid['c_depth']).mean()
grid['LT'] = grid['LT'].interpolate().rolling(5).mean().abs()

deployment_name2 = 'deploy2_';
LT_array2 = []
depth_array2 = []
profile_array2 = []
grid2 = pd.DataFrame(columns=['LT2','c_depth2']) # Note that there are now row data inserted.for i in range(0,58,2):

for i in range(0,10,2):
	c_file2 = 'C'+("%07d" % (i,))
	c_data2 = pd.read_pickle(directory+deployment_name2+file_type+c_file2)

	[LT2,Td2,Nsqu2,Lo2,R2,x_sorted2,idxs2] = TKED.thorpe_scales1(c_data2["c_depth"].values*-1,c_data2['c_dens'].values,full_output=True)
	
	c_data2['LT2'] = LT2
	grid2 = pd.concat([grid2,c_data2])

	# plt.plot(LT,c_data["c_depth"].values)
	# plt.xlabel("Thorpe_scales (m)")
	# plt.ylabel('Depth (m)')

	# plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	# plt.clf()
	#plt.show()
grid2['c_depth'] = grid2['c_depth'].round(0)
grid2 = grid2.groupby(grid2['c_depth']).mean()
grid2['LT2'] = grid2['LT2'].interpolate().rolling(5).mean().abs()


plt.plot(grid['LT'],grid['c_depth'],c='k')
plt.plot(grid2['LT2'],grid2['c_depth'],c='b')
plt.ylabel("Depth (m)")
plt.xlabel("Thorpe Scale (m)")
plt.legend(("deployment 1", "deployment 2"))
plt.show()