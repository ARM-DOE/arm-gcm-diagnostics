from matplotlib.pyplot import grid
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os,sys
import config

def DC_amip_line_harmonicD_plot():
    """Prepare line and harmonic Dial diagram for diurnal cycle of precipitation"""
    mod = config.modelname
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    modellist=['MIROC5','CMCC-CM','inmcm4','CCSM4','GFDL-HIRAM-C180','GFDL-HIRAM-C360','FGOALS-s2','HadGEM2-A','ACCESS1-0','ACCESS1-3']
    vas=['pr']
    for va_ind in range(len(vas)):
        pr_obs3=np.loadtxt(basedir+'observation/'+vas[va_ind]+'_JJA_DC_obs.csv')
        pr_cmip3=np.loadtxt(basedir+'cmip/'+vas[va_ind]+'_JJA_DC_model_regrid_3x3_correct.csv')
        pr_cmip3=pr_cmip3.reshape((3,len(modellist),8))
        pr_mod3=np.loadtxt(basedir+'model/'+vas[va_ind]+'_JJA_DC_'+mod+'_regrid_3x3_correct.csv')
        
        month=['Jun','Jul','Aug']
        mod_phase=np.empty([len(modellist)+1])
        mod_amp=np.empty([len(modellist)+1])
        for mon_id in range(len(month)):
            pr_obs=pr_obs3[mon_id,:]
            pr_mod=pr_mod3[mon_id,:]
            pr_cmip=pr_cmip3[mon_id,:,:]
               
        #
            fig0 = plt.figure()
            ax0=fig0.add_axes([0.14, 0.14, 0.84, 0.84])
            xax_3r=np.array([3.0*x-6.5 for x in range(8)])
            xax_cf=np.array([1.0*x-6.5 for x in range(24)])  #convert from GMT to LST -6.5 form SGP
            for mod in range(len(modellist)+1):
                if mod != len(modellist):
                    pr_day=pr_cmip[mod,:]
                else:
                    pr_day=pr_mod
            
                def func24(x, p1,p2):
                  return p1*np.sin(2*np.pi/24*x+p2)
            
                popt, pcov = curve_fit(func24, xax_3r, pr_day,p0=(1.0,0.2))
                p1_mod = popt[0]
                p2_mod = popt[1]
            
                ymod_fit=func24(xax_cf,p1_mod,p2_mod)+np.mean(pr_day)
                if mod != len(modellist) :
                    mod_fit,=ax0.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ymod_fit,ymod_fit)), 'grey',lw=1)
                if mod ==  len(modellist):
                    mod_fit,=ax0.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ymod_fit,ymod_fit)),'r', label = 'MOD',lw=2)
                    ax0.plot(np.concatenate((xax_3r,[x+24 for x in xax_3r])),np.concatenate((pr_day,pr_day)),'.r',label='MOD',lw=2,markersize=15)
            
                mod_amp[mod]=p1_mod
                if p1_mod<=0 :
                   p2_mod=1.5*np.pi-p2_mod
                if p1_mod>0 :
                   p2_mod=0.5*np.pi-p2_mod
                mod_phase[mod]=p2_mod
            
            #####################observation
            xax=np.array([1.0*x for x in range(24)])
            def func24(x, p1,p2):
              return p1*np.sin(2*np.pi/24*x+p2)
            
            ydata_cf=[x*24.0 for x in pr_obs]
            popt, pcov = curve_fit(func24, xax_cf, ydata_cf,p0=(1.0,0.2))
            p1_cf = popt[0]
            p2_cf = popt[1]
            obs2,=plt.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ydata_cf,ydata_cf)),'k.',label='OBS',lw=2,markersize=15)
            yobs2=func24(xax_cf,p1_cf,p2_cf)+np.mean(ydata_cf)
            obs_fit2,=plt.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])), np.concatenate((yobs2,yobs2)),'k',lw=2)
            
            my_xticks=['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h']
            my_xticks_loc=np.array([3*x for x in range(8)])
            plt.xticks(my_xticks_loc, my_xticks)
            ax0.set_xlim([0,24])
            ax0.set_ylim([-0.5,7])
            ax0.text(0.3, 0.95,'OBS',color='k',verticalalignment='top', horizontalalignment='left',transform=ax0.transAxes)
            ax0.text(0.3, 0.85,'MOD',color='r',verticalalignment='top', horizontalalignment='left',transform=ax0.transAxes)
            plt.xlabel('local solar time [hr]')
            plt.ylabel('precipitation at surface [mm/day]')
            
            ##########Generate hormonic dial plot: mapping phase and amplitude to Dial
        
            obs2_amp=abs(p1_cf)
            obs2_phase=0.5*np.pi-p2_cf  #-5.0/24*2*np.pi
            fig2 = plt.figure()
            ax2  =fig2.add_axes([0.1, 0.1, 0.8, 0.8],polar=True)#, axisbg='#d5de9c')
            
            size=50
            ax2.scatter(obs2_phase,obs2_amp,color='k',label='OBS',s=size*2)
            ax2.scatter(mod_phase[0:-2],abs(mod_amp[0:-2]),color='grey',s=size)
            ax2.scatter(mod_phase[-1],abs(mod_amp[-1]),color='r',label='MOD',s=size*2)
            ax2.legend(scatterpoints=1,loc='center right',bbox_to_anchor=(1.2,0.90),prop={'size':15})
            ax2.set_rmax(3)
            ax2.set_theta_direction(-1)
            ax2.set_theta_offset(np.pi/2)
            ax2.set_xticklabels(['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h'])
            grid(True)
            
            fig0.savefig(basedir+'figures/DC_amip_'+vas[va_ind]+'_'+month[mon_id]+'_line.png')
            fig2.savefig(basedir+'figures/DC_amip_'+vas[va_ind]+'_'+month[mon_id]+'_harmonicD.png')
    plt.close('all')




