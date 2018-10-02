import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_bins/';
deployment_name = 'deploy1_';
measurement_type = 'euler_';
file_type = 'raw_'
bin_number = 100

for i in range(2):
	a_file = 'A'+("%07d" % (i,))
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)