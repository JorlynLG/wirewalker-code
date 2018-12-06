import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ocean_tools import TKED

directory = '../../Data/deployment_raw/';
outdir = '../../plots/ctd/thorpe/';
deployment_name = 'deploy1_';
measurement_type = 'ctd_';
file_type = 'raw_'

i = 0
c_file = 'C'+("%07d" % (i,))
c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales1(c_data["c_depth"].values*-1,c_data['c_dens'].values,full_output=True)
	
eps = 0.64*(LT**2)*(Nsqu)**(3/2)

plt.plot((Nsqu))
plt.ylabel("Depth (m)")
plt.xlabel("Thorpes Scale (m)")
plt.show()