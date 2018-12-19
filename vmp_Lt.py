import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ocean_tools import TKED
import gsw
from scipy.io import loadmat 
import seawater

directory = '../../../RV Investigator/VMP/';
outdir = '../../plots/vmp/';



for i in range(1):
	data = loadmat(directory+'COOKI001.mat')



	#print(data['JAC_C'].shape)
	#data[JAC_C].reshape(500,)
	# df = pd.DataFrame({'cond':data['JAC_C'][5000:15000].tolist(),'temp':data['JAC_T'][5000:15000].tolist(),'pres':data['P'][5000:15000].tolist()})
	# #plt.plot(data['JAC_T'][5000:15000],-data['P'][5000:15000])
	# #plt.plot(-data['P'][5000:15000])
	# #plt.show()
	# df.groupby(df.index//2).mean()
	# # print(df)

	# cond = data['JAC_C'][5000:15000].reshape(500,20).mean(1)
	# temp = data['JAC_T'][5000:15000].reshape(500,20).mean(1)
	# pres = data['P_slow'][5000:15000].reshape(500,20).mean(1)
	cond = data['JAC_C'][141000:155000].reshape(700,20).mean(1)
	temp = data['JAC_T'][141000:155000].reshape(700,20).mean(1)
	pres = data['P_slow'][141000:155000].reshape(700,20).mean(1)
	plt.plot(data['P_slow'])
	plt.show()

	# cond = data['JAC_C'][5000:20000]
	# temp = data['JAC_T'][5000:20000]
	# pres = data['P_slow'][5000:20000]

	# salt = seawater.salt(cond,temp,pres)
	# # plt.plot(salt)
	# # plt.show()

	sal = gsw.SP_from_C(cond,temp,pres)
	# # plt.plot(cond)
	# # plt.show()
	# # plt.plot(temp)
	# # plt.show()
	# plt.plot(pres)
	# plt.show()
	# # plt.plot(sal)
	# # plt.show()


	# plt.plot(sal)
	# plt.show()
	CT = gsw.CT_from_t(sal,temp,pres)
	SA = gsw.SA_from_SP(sal,pres,174,-43)
	dens = gsw.sigma0(SA, CT)
	depth = gsw.z_from_p(pres,-43)
	dens = np.squeeze(dens)
	depth = np.squeeze(depth)
	[LT,Td,Nsqu,Lo,R,x_sorted,idxs] = TKED.thorpe_scales(depth,dens,full_output=True)

	# plt.plot(sal)
	# plt.show()

	# Tdd = pd.Series(Td)
	# Tdd = Tdd.rolling(100).mean()
	# Tdd = Tdd**2
	# Tdd = Tdd.rolling(100).mean()
	# Tdd = np.sqrt(Tdd)
	# plt.plot(Tdd)

	#plt.show()
	fig2, (ax2, ax3, ax4) = plt.subplots(1,3,sharey=True)
	# Temperature
	ax2.plot(dens,depth,c='k')
	ax2.set_ylabel('Depth (m)')
	#ax2.set_ylim(ax2.get_ylim()[::-1]) #this reverses the yaxis (i.e. deep at the bottom)
	ax2.set_xlabel('Density (kg/m3)')
	ax2.xaxis.set_label_position('top') # this moves the label to the top
	ax2.xaxis.set_ticks_position('top') # this moves the ticks to the top
	# Salinity
	ax3.plot(LT,depth,c='k')
	ax3.set_xlabel('LT (m)')
	ax3.xaxis.set_label_position('top') # this moves the label to the top
	ax3.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax3.yaxis.set_visible(False) # This erases the y ticks
	# Fluorescence
	ax4.plot(R,depth,c='k')
	ax4.axvline(x=0.25, c='b')
	ax4.set_xlabel('Overturn (Ro)')
	ax4.xaxis.set_label_position('top') # this moves the label to the top
	ax4.xaxis.set_ticks_position('top') # this moves the ticks to the top
	ax4.yaxis.set_visible(False) # This erases the y ticks	

	plt.show()
	# plt.savefig(outdir+measurement_type+deployment_name+'profile'+str(i)+".png")
	# plt.clf()
