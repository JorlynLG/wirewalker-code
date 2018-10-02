from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import figaspect, Figure
import gsw

directory = '../../Data/deployment_raw/';
outdir = '../../plots/eng/All/';
deployment_name = 'deploy1_';
measurement_type = 'eng_';
file_type = 'raw_'

for i in range(10,11):
	c_file = 'C'+("%07d" % (i,))
	c_data = pd.read_pickle(directory+deployment_name+file_type+c_file)

	e_file = 'E'+("%07d" % (i,))
	e_data = pd.read_pickle(directory+deployment_name+file_type+e_file)
	e_data['e_depth'] = pd.Series(gsw.z_from_p(e_data["e_pres"].values,-43), index=e_data.index)	
	
	w, h = figaspect(.25)
	fig = plt.Figure(figsize=(w,h))
	

	host = host_subplot(111, axes_class=AA.Axes)
	plt.subplots_adjust(bottom=.25)

	
	ax1 = host.twiny()
	ax2 = host.twiny()
	ax3 = host.twiny()
	ax4 = host.twiny()
	ax5 = host.twiny()

	new_fixed_axis = ax1.get_grid_helper().new_fixed_axis
	ax1.axis["bottom"] = new_fixed_axis(loc="bottom", axes=ax1,offset=(0,-30))
	new_fixed_axis = ax2.get_grid_helper().new_fixed_axis
	ax2.axis["bottom"] = new_fixed_axis(loc="bottom", axes=ax2,offset=(0,-60))
	new_fixed_axis = ax3.get_grid_helper().new_fixed_axis
	ax3.axis["bottom"] = new_fixed_axis(loc="bottom", axes=ax3,offset=(0,-90))
	new_fixed_axis = ax4.get_grid_helper().new_fixed_axis
	ax4.axis["top"] = new_fixed_axis(loc="top", axes=ax4,offset=(0,0))
	new_fixed_axis = ax5.get_grid_helper().new_fixed_axis
	ax5.axis["top"] = new_fixed_axis(loc="top", axes=ax5,offset=(0,30))


	host.set_ylabel("Depth (m)")
	host.set_xlabel("Turbidity (mV)")
	ax1.set_xlabel("Chlorophyll")
	ax2.set_xlabel("Par (mV)")
	ax3.set_xlabel("CDOM")
	ax4.set_xlabel("Temperature (C)")
	ax5.set_xlabel("Salinity (pss)")

	p1, = host.plot(e_data['e_turb'], e_data['e_depth'], label="Turbidity")
	p2, = ax1.plot(e_data['e_chl'], e_data['e_depth'], label="Chlorophyll")
	p3, = ax2.plot(e_data['e_par'], e_data['e_depth'], label="PAR")
	p4, = ax3.plot(e_data['e_cdom'], e_data['e_depth'], label="CDOM")
	p5, = ax4.plot(c_data['c_temp'], c_data['c_depth'], label="Temperature")
	p6, = ax5.plot(c_data['c_sal'], c_data['c_depth'], label="Salinity")

	host.set_xlim(0,700)
	ax1.set_xlim(70, 180)
	ax2.set_xlim(0, 800)
	ax3.set_xlim(55, 69)

	host.legend()

	host.axis["bottom"].label.set_color(p1.get_color())
	ax1.axis["bottom"].label.set_color(p2.get_color())
	ax2.axis["bottom"].label.set_color(p3.get_color())
	ax3.axis["bottom"].label.set_color(p4.get_color())
	ax4.axis["top"].label.set_color(p5.get_color())
	ax5.axis["top"].label.set_color(p6.get_color())
	

	plt.show()
	#plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	#plt.clf()
#savefig(gcf,[outdir,'/',measurement_type, deployment_name,'profile',num2str(stas(mm))])