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

for i in range(0,20,1):
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
plt.plot(grid['LT'],grid['c_depth'],c='k')
plt.ylabel("Depth (m)")
plt.xlabel("Thorpes Scale (m)")
plt.show()