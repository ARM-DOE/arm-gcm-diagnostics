import os,sys
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import csv
import config

mod = config.modelname
def AC_DC_cl_p_plot():
    """Prepare annual cycle and diurnal cycle plots of cloud fraction fro set 3 and set 5 diag"""
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    vas=['cl_p']
    month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for va_ind in range(len(vas)):
        pr_obs=np.loadtxt(basedir+'observation/'+vas[va_ind]+'_obs.csv')
        pr_obs=pr_obs.reshape((12,24,37))
        pr_mod=np.loadtxt(basedir+'model/'+vas[va_ind]+'_'+mod+'_regrid_3x3_correct.csv')
        pr_mod=pr_mod.reshape((12,8,37))
        
        cl_ob=np.nanmean(pr_obs,axis=1)
        cl_p=np.nanmean(pr_mod,axis=1)
        cl_ob_diurnal=np.nanmean(pr_obs,axis=0)
        cl_p_diurnal=np.nanmean(pr_mod,axis=0)
        cl_ob_ann=np.nanmean(cl_ob,axis=0)
        cl_p_ann=np.nanmean(cl_p,axis=0)
        ####################Monthly Mean Diurnal Cycle
        
        for index in range(2):
            fig1, axs = plt.subplots(4,3, figsize=(15, 12), facecolor='w', edgecolor='k',sharex=True,sharey=True)
            fig1.subplots_adjust(hspace = .3, wspace=.1)
            axs = axs.ravel()
            for imon in range(12):
                if index==0:
                     title='obs_'+vas[va_ind]+'_mon_diurnal_clim'
                     yy=np.linspace(0,23,24)
                     xx=np.linspace(100,1000,37)
                     x,y=np.meshgrid(xx,yy)
                     pr_obs_con=np.concatenate((pr_obs[imon,:,:],pr_obs[imon,:,:]),axis=0)#6 hour GMT to Local time
                     im=axs[imon].pcolormesh(y,x,pr_obs_con[6:30,::-1], vmin=0, vmax=25)
                     plt.xlim([0,23])
                     xax =  np.arange (0,24,3)
                     my_xticks = ['0','3','6','9','12','15','18','21']
           
                else:
                     title='mod_'+vas[va_ind]+'_mon_diurnal_clim'
                     yy=np.linspace(0,7,8)
                     xx=np.linspace(100,1000,37)
                     x,y=np.meshgrid(xx,yy)
                     pr_obs_con=np.concatenate((pr_mod[imon,:,:],pr_mod[imon,:,:]),axis=0)
                     #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
                     im=axs[imon].pcolormesh(y,x,pr_obs_con[1:9,::-1], vmin=0, vmax=25)
                     plt.xlim([0,7])
                     xax =  np.arange (0,8,1)
                     my_xticks = ['0','3','6','9','12','15','18','21']
        
                axs[imon].set_title(month[imon])
                plt.xticks(xax, my_xticks)
                plt.setp(axs[imon].get_xticklabels(), visible=True)
            for ax in axs[9:12]:
                ax.set_xlabel('Local time (hr)')
            for ax in axs[::3]:
                ax.set_ylabel('Pressure (mb)')
            axs[0].invert_yaxis()
            plt.suptitle(title)
            fig1.subplots_adjust(right=0.8)
            cbar_ax = fig1.add_axes([0.85, 0.15, 0.05, 0.7])
            fig1.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            fig1.savefig(basedir+'figures/'+title+'.png')
            plt.close('all')
        
        ##########################Diurnal cycle
        
        for index in range(2):
            fig2 = plt.figure()# Create figure
            ax  =fig2.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
            if index==0:
                 title='obs_'+vas[va_ind]+'_diurnal_clim'
                 yy=np.linspace(0,23,24)
                 xx=np.linspace(100,1000,37)
                 x,y=np.meshgrid(xx,yy)
                 pr_obs_con=np.concatenate((cl_ob_diurnal,cl_ob_diurnal),axis=0)#6 hour GMT to Local time
                 im=ax.pcolormesh(y,x,pr_obs_con[6:30,::-1], vmin=0, vmax=25)
                 plt.xlim([0,23])
                 xax =  np.arange (0,24,3)
                 my_xticks = ['0','3','6','9','12','15','18','21']
        
            else:
                 title='mod_'+vas[va_ind]+'_diurnal_clim'
                 yy=np.linspace(0,7,8)
                 xx=np.linspace(100,1000,37)
                 x,y=np.meshgrid(xx,yy)
                 pr_obs_con=np.concatenate((cl_p_diurnal,cl_p_diurnal),axis=0)
                 #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
                 im=ax.pcolormesh(y,x,pr_obs_con[1:9,::-1], vmin=0, vmax=25)
                 plt.xlim([0,7])
                 xax =  np.arange (0,8,1)
                 my_xticks = ['0','3','6','9','12','15','18','21']
        
            plt.xticks(xax, my_xticks)
            plt.ylabel('Pressure (mb)')
            plt.xlabel('Local time (hr)')
            plt.gca().invert_yaxis()
            plt.suptitle(title)
            cbar_ax = fig2.add_axes([0.85, 0.15, 0.05, 0.75])
            fig2.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            fig2.savefig(basedir+'figures/'+title+'.png')
        #    
            plt.close('all')
        ##########################Annual cycle
        
        yy=np.linspace(0,11,12)
        xx=np.linspace(100,1000,37)
        x,y=np.meshgrid(xx,yy)
        for index in range(3):
            fig = plt.figure()# Create figure
            ax  =fig.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
            if index==0:
                title='obs_'+vas[va_ind]+'_annual_cycle_clim'
                im=ax.pcolormesh(y,x,cl_p[:,::-1], vmin=0, vmax=25)
            elif index==1:
                im=ax.pcolormesh(y,x,cl_ob[:,::-1], vmin=0, vmax=25)
                title='mod_'+vas[va_ind]+'_annual_cycle_clim'
            elif index==2:
                im=ax.pcolormesh(y,x,cl_p[:,::-1]-cl_ob[:,::-1], vmin=-10, vmax=10)
                title='diff_'+vas[va_ind]+'_annual_cycle_clim'
            xax =  np.arange (0,12,1)
            my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
            plt.xticks(xax, my_xticks)
            plt.xlim(0,11)
            plt.ylabel('Pressure (mb)')
            plt.gca().invert_yaxis()
            plt.suptitle(title)
            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.75])
            fig.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            fig.savefig(basedir+'figures/'+title+'.png')
        #    
            plt.close('all')
            
        ###########################Seasonal Mean
        levels=xx
        seasons=['MAM','JJA','SON','DJF']
        cl_p2=np.concatenate((cl_p,cl_p),axis=0)
        cl_ob2=np.concatenate((cl_ob,cl_ob),axis=0)
        for index in range(len(seasons)):
           
            fig3 = plt.figure()# Create figure
            ax  =fig3.add_axes([0.15, 0.1, 0.8, 0.8]) # Create axes
            ax.plot(np.nanmean(cl_p2[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'r',lw=3,label='MOD')
            ax.plot(np.nanmean(cl_ob2[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'k',lw=3,label='OBS')
            plt.gca().invert_yaxis()
            plt.ylabel('Pressure (mb)')
            plt.xlabel('Cloud fraction (%)')
            plt.xlim([0,25])
            plt.legend(loc='best',prop={'size':15})
            plt.title(seasons[index]+' Mean Cloud Fraction')
            fig3.savefig(basedir+'figures/'+seasons[index]+'_'+vas[va_ind]+'_diff.png')
            plt.close('all')
        
        ###########################ANN Mean
        
        
        fig0 = plt.figure()# Create figure
        ax  =fig0.add_axes([0.15, 0.1, 0.8, 0.8]) # Create axes
        ax.plot(cl_p_ann[::-1],levels,'r',lw=3,label='MOD')
        ax.plot(cl_ob_ann[::-1],levels,'k',lw=3,label='OBS')
        plt.gca().invert_yaxis()
        plt.ylabel('Pressure (mb)')
        plt.xlabel('Cloud fraction (%)')
        plt.xlim([0,25])
        plt.legend(loc='best',prop={'size':15})
        plt.title('Annual Mean Cloud Fraction')
        fig0.savefig(basedir+'figures/ANN_'+vas[va_ind]+'_diff.png')
        plt.close('all')
