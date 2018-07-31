import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

directory = '../../Data/deployment_raw/';
out_directory = '../../plots/adcp_aqua/euler_plots/';
deployment_name = 'deploy1_';
measurement_type = 'euler_';
file_type = 'raw_'

for i in range(0,58,2):
	a_file = 'A'+("%07d" % (i,))
	a_data = pd.read_pickle(directory+deployment_name+file_type+a_file)
	fig, axes = plt.subplots(nrows=3, ncols=1)

	#heading-plot
	unwrapped = np.unwrap(a_data["a_heading"].apply(np.radians).values)
	a_data['a_heading'] = pd.Series(unwrapped, index=a_data.index)
	ax1 = a_data.plot(x="a_time",y="a_heading",ax=axes[0],legend=False)
	ax1.set_ylabel('heading (degree)')
	#roll-plot
	ax2 = a_data.plot(x="a_time",y="a_roll",ax=axes[1],legend=False)
	ax2.set_ylabel('roll (degree)')
	#pitch-plot
	ax3 = a_data.plot(x="a_time",y="a_pitch",ax=axes[2],legend=False)
	ax3.set_ylabel('pitch (degree)')
	ax3.set_xlabel('time')
	fig.suptitle("Profile "+ str(i))

	#Save and close figure
	plt.savefig(out_directory+"adcp_"+deployment_name+'profile'+str(i)+".png")
	plt.close()