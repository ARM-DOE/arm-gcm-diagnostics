import os
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid
from varid_dict import varid_longname
from cdtime import *
from scipy.optimize import curve_fit

def var_diurnal_cycle(var, season):
    "Calculate diurnal cycle climatology of each variable"
    if season == 'JJA':
        mo0 = 6
    if season == 'SON': 
        mo0 = 9
    if season == 'DJF': 
        mo0 = 12
    if season == 'MAM': 
        mo0 = 3
    years = range(1979,2006)         
    var_dc_year = np.empty([len(years),8])*np.nan
    for iy,year in enumerate(years):
        t1 = comptime(year,mo0,01)
        t2 = t1.add(90,Days)
#        try:
        var_yr =  var(time=(t1,t2,'co'))
        var_dc_year[iy,:]= np.nanmean(np.reshape(var_yr,(90,8)), axis=0)
        if var.id == 'tas':
            var_dc_year[iy,:] = var_dc_year[iy,:]-273.15

        if var.id == 'pr':
            var_dc_year[iy,:] = var_dc_year[iy,:]*3600.*24.
#        print year
#        except:
#            print str(year) +' not Available!'
#            var_dc_year[iy,:] =  np.nan
    var_dc = np.nanmean(var_dc_year,axis=0)  
    return var_dc


def diurnal_cycle_data(parameter):
    """Calculate diurnal cycle climatology"""
    variables = parameter.variables
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    seasons = parameter.season
   
    test_model = parameter.test_data_set 
    ref_models = parameter.ref_models

    # Calculate for test model
    
    test_var_season=np.empty([len(variables),8])*np.nan
    test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*3hr*.nc')) #read in 3hr test data
    fin = cdms2.open(test_file[0])
    
    print 'test_model',test_model

    for j, variable in enumerate(variables): 
        for season in seasons:
            try:
                var = fin (variable,squeeze = 1)
                test_var_dc = var_diurnal_cycle(var,season)
                #print test_var_dc

            except:
                print (variable+" not processed for " + test_model)
            test_var_season[j,:] = test_var_dc

    # Calculate for observational data
    obs_var_season=np.empty([len(variables),24])*np.nan
    #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_domain_diurnal*.nc')) #read in diurnal test data
    #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_diurnal*.nc')) #read in diurnal test data
    obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_diurnal_climo_sgp_localtime.nc')) #read in diurnal test data
    print 'ARM data'
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
              
        try:
            var = fin (variable)
            print var.shape
            var_dc = np.reshape(var,(12,24))
 
            print seasons,var_dc
            for season in seasons:
                if season == 'JJA':
                    obs_var_dc = np.nanmean(var_dc[5:8,:],axis=0)

            if var.id == 'tas':
                obs_var_dc = obs_var_dc-273.15
    
            if var.id == 'pr':
                obs_var_dc = obs_var_dc*3600.*24.
            #print obs_var_dc 
        except:
            print (variable+" not processed for obs")
        obs_var_season[j,:] = obs_var_dc

    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),8])*np.nan
 
    for i, ref_model in enumerate(ref_models):
         ref_file = glob.glob(os.path.join(cmip_path,'*'+ref_model+'*3hr*.nc')) #read in monthly cmip data
         print 'ref_model', ref_model
         if not ref_file :
             print (ref_model+" not found!") 
         else:
             fin = cdms2.open(ref_file[0])
         
             for j, variable in enumerate(variables): 
                 for season in seasons:
                     try:
                         var = fin (variable,squeeze = 1)
                         cmip_var_season[i, j, :] = var_diurnal_cycle(var, season)

                     except:
                         print (variable+" not processed for " + ref_model)
             fin.close()  
    # Calculate multi-model mean
    mmm_var_season =  np.nanmean(cmip_var_season,axis=0)

    # Save data in csv format in metrics folder
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_test_diurnal_cycle.csv',test_var_season[j,:])
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_mmm_diurnal_cycle.csv',mmm_var_season[j,:])
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_cmip_diurnal_cycle.csv',cmip_var_season[:,j,:])
            np.savetxt(output_path+'/metrics/'+variable+'_'+season+'_obs_diurnal_cycle.csv',obs_var_season[j,:])

    


def func24(x,p1,p2):
     return p1*np.sin(2*np.pi/24*x+p2)

def diurnal_cycle_plot(parameter):
    """Calculate diurnal cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    ref_models = parameter.ref_models

    var_longname = [ varid_longname[x] for x in variables]
    mod_num = len(ref_models)
    
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            test_data = genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_test_diurnal_cycle.csv')
            mmm_data =  genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_mmm_diurnal_cycle.csv')
            obs_data =  genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_obs_diurnal_cycle.csv')
            cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_'+season+'_cmip_diurnal_cycle.csv')
            mod_num = cmip_data.shape[0]
    
            fig = plt.figure()# Create figure
            ax  =fig.add_axes([0.15, 0.14, 0.8, 0.8]) # Create axes
            xax_3hr=np.array([3.0*x-6.5 for x in range(8)])
            xax_1hr=np.array([1.0*x-6.5 for x in range(24)]) 
            #xax =  np.arange (1,13,1)
    
            # plotting ref models 
            mod_phase=np.empty([mod_num])
            mod_amp=np.empty([mod_num])
            for mod_ind in range(mod_num):
                popt, pcov = curve_fit(func24, xax_3hr, cmip_data[mod_ind,:] ,p0=(1.0,0.2))
                p1_mod = popt[0]
                p2_mod = popt[1]
                ymod_fit=func24(xax_1hr,p1_mod,p2_mod)+np.mean(cmip_data[mod_ind,:])
                
                mod_fit,=ax.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((ymod_fit,ymod_fit)), 'grey',lw=1)
                mod_amp[mod_ind]=p1_mod
                if p1_mod<=0 :
                   p2_mod=1.5*np.pi-p2_mod
                if p1_mod>0 :
                   p2_mod=0.5*np.pi-p2_mod
                mod_phase[mod_ind]=p2_mod
                #ax.plot(xax_3hr,cmip_data[mod_ind,:],'grey',lw=1)
    
            # plotting test model
            ann_mean=np.mean(test_data[:])
            popt, pcov = curve_fit(func24, xax_3hr, test_data ,p0=(1.0,0.2))
            p1_mod = popt[0]
            p2_mod = popt[1]
            ymod_fit=func24(xax_1hr,p1_mod,p2_mod)+np.mean(test_data)
            mod_fit,=ax.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((ymod_fit,ymod_fit)), 'r',label = 'MOD: %.2f'%ann_mean,lw=2)
            ax.plot(np.concatenate((xax_3hr,[x+24 for x in xax_3hr])),np.concatenate((test_data,test_data)),'.r',label='MOD',lw=2,markersize=15)
            test_amp=p1_mod
            if p1_mod<=0 :
               p2_mod=1.5*np.pi-p2_mod
            if p1_mod>0 :
               p2_mod=0.5*np.pi-p2_mod
            test_phase=p2_mod
            #ax.plot(xax_3hr,test_data[:],'r',label='MOD: %.2f'%ann_mean,lw=3)
    
            # plotting test model
            ann_mean=np.mean(obs_data[:])
            popt, pcov = curve_fit(func24, xax_1hr, obs_data ,p0=(1.0,0.2))
            p1_obs = popt[0]
            p2_obs = popt[1]
            yobs2=func24(xax_1hr,p1_obs,p2_obs)+np.mean(obs_data)
            obs2,=plt.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((obs_data,obs_data)),'k.',label='OBS: %.2f'%ann_mean,lw=2,markersize=15)
            obs_fit2,=plt.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])), np.concatenate((yobs2,yobs2)),'k',lw=2)
            obs2_amp=abs(p1_obs)
            obs2_phase=0.5*np.pi-p2_obs  #-5.0/24*2*np.pi
    
            #ax.plot(xax_1hr,obs_data[:],'k',label='OBS: %.2f'%ann_mean,lw=3)
            #ann_mean=np.mean(mmm_data[:])
            #ax.plot(xax_3hr,mmm_data[:],'b',label='MMM: %.2f'%ann_mean,lw=3)
            my_xticks=['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h']
            my_xticks_loc=np.array([3*x for x in range(8)])
            plt.xticks(my_xticks_loc, my_xticks)
            ax.set_xlim([0,24])
            ax.set_ylim([-0.5,7])
            ax.text(0.3, 0.95,'OBS',color='k',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)
            ax.text(0.3, 0.85,'MOD',color='r',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)
            plt.xlabel('local solar time [hr]')
            plt.ylabel(var_longname[j])
            fig.savefig(output_path+'/figures/'+variable+'_'+season+'_diurnal_cycle.png')
            plt.close('all')
           
    
    
            ##########Generate hormonic dial plot: mapping phase and amplitude to Dial
    
            fig2 = plt.figure()
            ax2  =fig2.add_axes([0.1, 0.1, 0.8, 0.8],polar=True)#, axisbg='#d5de9c')
    
            size=50
            ax2.scatter(obs2_phase,obs2_amp,color='k',label='OBS',s=size*2)
            ax2.scatter(mod_phase[:],abs(mod_amp[:]),color='grey',s=size)
            ax2.scatter(test_phase,abs(test_amp),color='r',label='MOD',s=size*2)
            ax2.legend(scatterpoints=1,loc='center right',bbox_to_anchor=(1.2,0.90),prop={'size':15})
            ax2.set_rmax(3)
            ax2.set_theta_direction(-1)
            ax2.set_theta_offset(np.pi/2)
            ax2.set_xticklabels(['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h'])
            grid(True)
    
            fig2.savefig(output_path+'/figures/'+variable+'_'+season+'_diurnal_cycle_harmonic_diagram.png')


    


    
    
    
    
