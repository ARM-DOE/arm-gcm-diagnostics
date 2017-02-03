import os,sys
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import csv
import config

mod = config.modelname
def AC_mean_amip_plot():
    """1. Make line plots of annual cycle for the 2nd set of diagnostics. 2. Prepare for data for tables in the 1st set of diagnostics."""

    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','ps','prw','cllvi','albedo']
    xaxis=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Surface Pressure (Pa)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Surface Albedo']
    
    xax =  np.arange (1,13,1)
    ylim=[(-5,45),(0,6),(10,80),(20,90),(-10,140),(0,160),(300,550),(240,440),(10,80),(100,350),(-25,35),(5,45),(-0.1,0.25),(0.0,0.3)]
    
    seasons=['DJF','MAM','JJA','SON','ANN']
    #sns=[2,5,8,11,0]
    sns=[11,2,5,8,0]
    pr_sns_data=np.empty([len(vas),len(seasons),5])*np.nan
    space='&nbsp;'
    for va_ind in range(len(vas)):
        fig = plt.figure()# Create figure
        ax  =fig.add_axes([0.15, 0.14, 0.8, 0.8]) # Create axes
        pr_cmip=genfromtxt(basedir+'cmip/all_'+vas[va_ind]+'_model_regrid_3x3_correct.csv')
        #pr_mod=genfromtxt(basedir+'model/'+vas[va_ind]+'_'+mod+'_regrid_3x3_correct.csv')
        pr_mod=genfromtxt(basedir+'model/all_'+vas[va_ind]+'_'+mod+'_regrid_3x3_correct.csv')
        #pr_obs=genfromtxt(basedir+'observation/all_'+vas[va_ind]+'_obs_regrid_3x3.csv')
        pr_obs=genfromtxt(basedir+'observation/all_'+vas[va_ind]+'_ac_obs.csv')
        pr_obs=pr_obs[0]
        mod_num=pr_cmip.shape[0]-1
        pr_mmm=pr_cmip[mod_num,:]
        for mod_ind in range(mod_num):
            ax.plot(xax,pr_cmip[mod_ind,:],'grey',lw=1)
        pr_ann=np.mean(pr_mod[:])
        ax.plot(xax,pr_mod[:],'r',label='MOD: %.2f'%pr_ann,lw=3)
        pr_ann=np.mean(pr_obs[:])
        ax.plot(xax,pr_obs[:],'k',label='OBS: %.2f'%pr_ann,lw=3)
        pr_ann=np.mean(pr_mmm[:])
        ax.plot(xax,pr_mmm[:],'b',label='MMM: %.2f'%pr_ann,lw=3)
        my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
        plt.xticks(xax, my_xticks)
        plt.xlim(1,12)
        plt.ylim(ylim[va_ind])
        plt.title('Annual Cycle: Model vs OBS vs AMIP5' )
        plt.xlabel('Month')
        plt.legend(loc='best',prop={'size':15})
        plt.ylabel(xaxis[va_ind])
        fig.savefig(basedir+'figures/AC_amip_'+vas[va_ind]+'.png')
        plt.close('all')
       
        pr_mod=np.concatenate((pr_mod,pr_mod),axis=1)
        pr_obs=np.concatenate((pr_obs,pr_obs),axis=1)
        pr_mmm=np.concatenate((pr_mmm,pr_mmm),axis=1)
        for si in range(len(seasons)):
            if seasons[si]!='ANN':
                pr_mod_sns=pr_mod[sns[si]:sns[si]+3]
                pr_obs_sns=pr_obs[sns[si]:sns[si]+3]
                pr_mmm_sns=pr_mmm[sns[si]:sns[si]+3]
            else:
                pr_mod_sns=pr_mod[0:12]
                pr_obs_sns=pr_obs[0:12]
                pr_mmm_sns=pr_mmm[0:12]
            #pr_sns_data[va_ind,si,:]=(np.mean(pr_mod_sns),np.mean(pr_obs_sns),np.mean(pr_mod_sns)-np.mean(pr_obs_sns),np.mean(pr_mmm_sns),np.sqrt(((pr_mod_sns - pr_obs_sns) ** 2).mean()))
            pr_sns_data[va_ind,si,:]=(round(np.mean(pr_mod_sns),3),round(np.mean(pr_obs_sns),3),round(np.mean(pr_mod_sns)-np.mean(pr_obs_sns),3),round(np.mean(pr_mmm_sns),3),round(np.sqrt(((pr_mod_sns - pr_obs_sns) ** 2).mean()),3))
    header=['Variables','Model','Obs','Model-Obs','CMIP5','RMSE']
#    header=[x+space*20 for x in header]
    for si in range(len(seasons)):
       with open(basedir+'metrics/'+mod+'_table_'+seasons[si]+'.csv','w') as f1:
               writer=csv.writer(f1, delimiter=',',lineterminator='\n', quoting=csv.QUOTE_NONE)
               writer.writerow(header)
               #use tuple to generate csv 
               writer.writerows([c]+row.tolist() for c, row in zip(xaxis,pr_sns_data[:,si,:]))

#               for i in range(len(vas)):
#                   row=['%-20s'%xaxis[i]+space*20 +'%20s'%str('%6.3f'%pr_sns_data[i,si,0])+space*20 +'%20s'%str('%6.3f'%pr_sns_data[i,si,1])+space*20 +'%20s'%str('%6.3f'%pr_sns_data[i,si,2])+space*20 +'%20s'%str('%6.3f'%pr_sns_data[i,si,3])+space*20 +'%20s'%str('%6.3f'%pr_sns_data[i,si,4])]
#                   writer.writerow(row )
#       np.savetxt(basedir+'metrics/'+mod+'_AC_amip_'+seasons[si]+'.csv',pr_sns_data[:,si,:],fmt='%.3f')#,delimiter=10*'&nbsp;')





