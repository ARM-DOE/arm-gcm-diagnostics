import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

def compute_metrics(homedir):

#    basedir='/g/g92/zhang40/calc_stats'
    basedir=homedir
    pr_mod=genfromtxt(basedir+'/model/'+'CESM-CAM5_AC.csv')
    
    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','net_sfc','prw','cllvi','net_rad','net_hf','albedo']
    vas=['tas','pr']
    xaxis=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Net Surface Energy flux (W/m2)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Surface Net Radiative Flux (W/m2)','Surface Net SH+LF Fluxes (W/m2)','Surface Albedo']
    xax =  np.arange (1,13,1)
    ylim=[(-5,45),(0,6),(10,80),(20,90),(-10,140),(0,160),(300,550),(240,440),(10,80),(100,350),(-25,35),(5,45),(-0.1,0.25),(0,200),(0,200),(0.05,0.3)]
    
    for va_ind in range(len(vas)):
       fig = plt.figure()# Create figure
       ax  =fig.add_axes([0.15, 0.14, 0.8, 0.8]) # Create axes
       pr_cmip=genfromtxt(basedir+'/cmip/all_'+vas[va_ind]+'_model_regrid_3x3.csv')
       pr_obs=genfromtxt(basedir+'/observation/all_'+vas[va_ind]+'_obs_regrid_3x3.csv')
       mod_num=pr_cmip.shape[0]-1
    #   ax.plot(err_cf[0:20,:],'lightgrey')
       for mod_ind in range(mod_num):
           ax.plot(xax,pr_cmip[mod_ind,:],'lightgrey',lw=1)
       pr_ann=np.mean(pr_mod[va_ind,:])
       ax.plot(xax,pr_mod[va_ind,:],'r',label='MOD: %.2f'%pr_ann,lw=3)
       pr_ann=np.mean(pr_obs[0,:])
       ax.plot(xax,pr_obs[0,:],'k',label='OBS: %.2f'%pr_ann,lw=3)
       pr_ann=np.mean(pr_cmip[mod_num,:])
       ax.plot(xax,pr_cmip[mod_num,:],'b',label='MMM: %.2f'%pr_ann,lw=3)
       my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
       plt.xticks(xax, my_xticks)
       plt.xlim(1,12)
       plt.ylim(ylim[va_ind])
       plt.title('Annual Cycle: Modle vs OBS vs AMIP5' )
       plt.xlabel('Month')
       plt.legend(loc='best',prop={'size':15})
       plt.ylabel(xaxis[va_ind])
       fig.savefig('../figures/AC_amip_'+vas[va_ind]+'.png')
    #fig.savefig('figures/AnnualCycle_mo_'+err_obs[obs]+'_SWDN_decomp_regrid_3x3.eps')
    
#    plt.show()




