#===========================================================================================================================
# Program for generate precipitation diurnal cycle from hourly data -- Originally written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov-Dec 2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### change the input/output format & the local time offset to site-dependent
    # ### minor fix on the plotting code for better visualization
    # ### change the default treatments when test model not found
    # ### extend the diurnal cycle to all the four seasons, and overlay MMM
    # ### phase calc. for Obs is fixed for accurate hamnoic plot position
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2022
    # ### add the auto-detection of testmodel temporal resolution (currently support 1-hr & 3hr)
    # ### add the user input of starting and ending years of making the testmodel climatology
    # --------------------------------------------------------------------------------------
#===========================================================================================================================
import os
import pdb
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid
from .varid_dict import varid_longname
import cdtime
from scipy.optimize import curve_fit

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def var_diurnal_cycle(var, season, tres, styr, edyr):
    "Calculate diurnal cycle climatology of each variable"
    if season == 'ANN':
        mo0 = 0
    if season == 'JJA':
        mo0 = 6
    if season == 'SON': 
        mo0 = 9
    if season == 'DJF': 
        mo0 = 12
    if season == 'MAM': 
        mo0 = 3
    #auto-adjust by the input resolution
    if tres=='1hr': tres_id=24
    if tres=='3hr': tres_id=8
    years = list(range(styr,edyr))         
    var_dc_year = np.empty([len(years),tres_id])*np.nan
    for iy,year in enumerate(years):
        t1 = cdtime.comptime(year,mo0,0o1)
        if season == 'ANN':
            t2 = t1.add(360,cdtime.Days)
        else:
            t2 = t1.add(90,cdtime.Days)
#        try:
        var_yr =  var(time=(t1,t2,'co'))
        #pdb.set_trace()
        if season == 'ANN':
            var_dc_year[iy,:]= np.nanmean(np.reshape(var_yr,(360,tres_id)), axis=0)
        else:
            var_dc_year[iy,:]= np.nanmean(np.reshape(var_yr,(90,tres_id)), axis=0)


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

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def diurnal_cycle_data(parameter):
    """Calculate diurnal cycle climatology"""
    variables = parameter.variables
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    seasons = parameter.season
   
    test_model = parameter.test_data_set 

    test_styr = parameter.test_start_year
    test_edyr = parameter.test_end_year

    ref_models = parameter.ref_models
 
    arm_name = parameter.arm_filename

    sites = parameter.sites

    cmip_ver = cmip_path.split('/')[-1]

    print('============================================================')
    print('Create Precipitation Diurnal Cycles: '+sites[0])
    print('============================================================')


    # Calculate for test model
    test_findex = 0 #preset of test model indicator
    
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*hr*.nc')) #read in 3hr test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        print(test_path,test_model,sites[0][:3]+test_model+'*hr' + sites[0][3:5].upper())
        test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'*hr' + sites[0][3:5].upper()+'*.nc' ))
    print('test_file: ',test_file)

    if len(test_file) == 0:
       print('No diurnal data for test model were found: '+sites[0])

    #test model exist
    if len(test_file) > 0:
        test_findex = 1 

        #initialize the indicator for temporal res of testmodel
        test_tres = test_file[0].split(test_model)[-1][:3] #e.g., '3hr', '1hr'
        print('test_tres: ',test_tres)

        fin = cdms2.open(test_file[0])
        if test_tres == '1hr': test_tidlen=24
        if test_tres == '3hr': test_tidlen=8

        test_var_dc = np.empty([test_tidlen])*np.nan
        test_var_season=np.empty([len(variables),test_tidlen,len(seasons)])*np.nan

        print(('Processing diurnal data for test_model',test_model,' with Tres of '+test_tres))

        for j, variable in enumerate(variables): 
            for k,season in enumerate(seasons):
                try:
                    var = fin (variable,squeeze = 1)
                    test_var_dc = var_diurnal_cycle(var,season,test_tres,test_styr,test_edyr)
                    test_var_season[j,:,k] = test_var_dc
                except:
                    print((variable+" "+season+" not processed for " + test_model))
                    print('!!please check the start and end year in basicparameter.py')
                    test_findex = 0
    
    # Calculate for observational data
    obs_var_season=np.empty([len(variables),24,len(seasons)])*np.nan
    #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_domain_diurnal*.nc')) #read in diurnal test data
    #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_diurnal*.nc')) #read in diurnal test data
    if not arm_name:
        #obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_c1_diurnal_climo_sgp_localtime.nc')) #read in diurnal test data
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag_domain_diurnal*.nc')) #read in diurnal test data
    else:
        #obs_file = glob.glob(os.path.join(obs_path,'sgparmdiagsmondiurnalC1.c1.nc'))
        obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsmondiurnal'+ sites[0][3:5].upper()+'.c1.nc'))
    print('ARM data')
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
              
        try:
            var = fin (variable)
            var_dc = np.reshape(var,(int(var.shape[0]/12/24),12,24))
            var_dc = np.nanmean(var_dc,axis=0)

            # extend the var for all seasons [XZ]
            var_dc12 = np.concatenate((var_dc,var_dc),axis=0)
            for k,season in enumerate(seasons):
                if season == 'ANN':
                    obs_var_dc = np.nanmean(var_dc12[0:12,:],axis=0)
                if season == 'MAM':
                    obs_var_dc = np.nanmean(var_dc12[2:5,:],axis=0)
                if season == 'JJA':
                    obs_var_dc = np.nanmean(var_dc12[5:8,:],axis=0)
                if season == 'SON':
                    obs_var_dc = np.nanmean(var_dc12[8:11,:],axis=0)
                if season == 'DJF':
                    obs_var_dc = np.nanmean(var_dc12[11:14,:],axis=0)

                # convert var units
                if var.id == 'tas':
                    obs_var_dc = obs_var_dc-273.15
                if var.id == 'pr':
                    obs_var_dc = obs_var_dc*3600.*24.
                # store processed array
                obs_var_season[j,:,k] = obs_var_dc
        except:
            print((variable+" "+season+" not processed for obs"))

    # Calculate cmip model seasonal mean climatology (diurnal cycles)
    cmip_var_season=np.empty([len(ref_models),len(variables),8,len(seasons)])*np.nan
    mmm_var_season=np.empty([len(variables),8,len(seasons)])*np.nan

    for i, ref_model in enumerate(ref_models):
         if not arm_name:
             ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+'*'+ref_model+'*3hr*.nc')) #read in monthly cmip data
         else:
             ref_model = cmip_ver +''.join(e for e in ref_model if e.isalnum()).lower()
             ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+sites[0][:3]+ref_model+'3hr'+sites[0][3:5].upper()+'*.nc' )) #read in monthly test data

         print(('ref_model', ref_model))
         if not ref_file :
             print((ref_model+" not found!"))
         else:
             fin = cdms2.open(ref_file[0])
         
             for j, variable in enumerate(variables): 
                 for k,season in enumerate(seasons):
                     try:
                         var = fin (variable,squeeze = 1)
                         cmip_var_season[i, j, :, k] = var_diurnal_cycle(var, season,'3hr',1979,2006)

                     except:
                         print((variable+" "+season+" not processed for " + ref_model))
             fin.close()

    # Calculate multi-model mean
    # TODO: cmip_var_season should only save available models, remove all rows with nan
    for k,season in enumerate(seasons):
        mmm_var_season[:,:,k] =  np.nanmean(cmip_var_season[:,:,:,k],axis=0)

    # Save data in csv format in metrics folder

    # create site-dependent folder [XZ]
    # Generate new folder given site names:
    if not os.path.exists(os.path.join(output_path,'metrics',sites[0])):
        os.makedirs(os.path.join(output_path,'metrics',sites[0]))
    for j, variable in enumerate(variables):
        for k, season in enumerate(seasons):
            print('===Check: ',test_findex)
            if test_findex == 1: np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_test_diurnal_cycle_'+test_tres+'_'+sites[0]+'.csv',test_var_season[j,:,k])
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_mmm_diurnal_cycle_'+sites[0]+'.csv',mmm_var_season[j,:,k])
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_cmip_diurnal_cycle_'+sites[0]+'.csv',cmip_var_season[:,j,:,k])
            np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_obs_diurnal_cycle_'+sites[0]+'.csv',obs_var_season[j,:,k])


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def func24(x,p1,p2):
     return p1*np.sin(2*np.pi/24*x+p2)

def diurnal_cycle_plot(parameter):
    """Calculate diurnal cycle climatology"""
    sites=parameter.sites
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    ref_models = parameter.ref_models

    var_longname = [ varid_longname[x] for x in variables]
    mod_num = len(ref_models)

    # create site-dependent folder [XZ]
    # Generate new folder given site names:
    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    # start the plotting procedure
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            # check the test model data
            test_findex = 0 #preset of test model indicator
            test_file = glob.glob(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_test_diurnal_cycle_*'+sites[0]+'.csv')
            if len(test_file) == 0:
               print('No test model plotted for diurnal cycle: '+sites[0])
            if len(test_file) > 0: 
                test_findex = 1   #test model exist
                test_tres = test_file[0].split('_test_diurnal_cycle_')[-1][:3] #e.g., '3hr', '1hr'

            # read data
            if test_findex == 1: test_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_test_diurnal_cycle_'+test_tres+'_'+sites[0]+'.csv')
            mmm_data =  genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_mmm_diurnal_cycle_'+sites[0]+'.csv')
            obs_data =  genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_obs_diurnal_cycle_'+sites[0]+'.csv')
            cmip_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_'+season+'_cmip_diurnal_cycle_'+sites[0]+'.csv')
            mod_num = cmip_data.shape[0]

            # plotting
            fig = plt.figure()# Create figure
            ax  =fig.add_axes([0.10, 0.10, 0.85, 0.85]) # Create axes
            #-----------------------------------------------------------------------------
            # create site-dependent time offset for the local time & plotting range [XZ]
            if sites[0] == 'sgpc1': local_offset=-6.5;  yup=10
            if sites[0] == 'enac1': local_offset=-2;    yup=6
            if sites[0] == 'nsac1': local_offset=-10;    yup=4
            # for positive offset-24h: make sure the plotting continuity
            if sites[0] == 'twpc1': local_offset=10-24; yup=30
            if sites[0] == 'twpc2': local_offset=11-24; yup=15
            if sites[0] == 'twpc3': local_offset=9-24;  yup=30
            if sites[0] == 'maom1': local_offset=-4;    yup=30
            xax_3hr=np.array([3.0*x+local_offset for x in range(8)])
            xax_1hr=np.array([1.0*x+local_offset for x in range(24)]) 
            #xax =  np.arange (1,13,1)
            #-----------------------------------------------------------------------------
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

            # plotting multi-model mean [XZ]
            ann_mean=np.mean(mmm_data[:])
            popt, pcov = curve_fit(func24, xax_3hr, mmm_data ,p0=(1.0,0.2))
            p1_mod = popt[0]
            p2_mod = popt[1]
            ymod_fit=func24(xax_1hr,p1_mod,p2_mod)+np.mean(mmm_data)
            ax.plot(np.concatenate((xax_3hr,[x+24 for x in xax_3hr])),np.concatenate((mmm_data,mmm_data)),'.b',label = 'MMM: %.2f'%ann_mean,lw=2,markersize=10)
            mod_fit,=ax.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((ymod_fit,ymod_fit)), 'b',label = 'MMM FFT',lw=2)
            mmm_amp=p1_mod
            if p1_mod<=0 :
               p2_mod=1.5*np.pi-p2_mod
            if p1_mod>0 :
               p2_mod=0.5*np.pi-p2_mod
            mmm_phase=p2_mod

            # plotting test model
            if test_findex == 1: 
                if test_tres == '1hr': test_pxaxis = xax_1hr.copy()
                if test_tres == '3hr': test_pxaxis = xax_3hr.copy()
                ann_mean=np.mean(test_data[:])
                popt, pcov = curve_fit(func24, test_pxaxis, test_data ,p0=(1.0,0.2))
                p1_mod = popt[0]
                p2_mod = popt[1]
                ymod_fit=func24(xax_1hr,p1_mod,p2_mod)+np.mean(test_data)
                ax.plot(np.concatenate((test_pxaxis,[x+24 for x in test_pxaxis])),np.concatenate((test_data,test_data)),'.r',label = 'MOD: %.2f'%ann_mean,lw=2,markersize=10)
                mod_fit,=ax.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((ymod_fit,ymod_fit)), 'r',label = 'MOD FFT',lw=2)
                test_amp=p1_mod
                if p1_mod<=0 :
                   p2_mod=1.5*np.pi-p2_mod
                if p1_mod>0 :
                   p2_mod=0.5*np.pi-p2_mod
                test_phase=p2_mod
                #ax.plot(xax_3hr,test_data[:],'r',label='MOD: %.2f'%ann_mean,lw=3)
    
            # plotting observation
            ann_mean=np.mean(obs_data[:])
            popt, pcov = curve_fit(func24, xax_1hr, obs_data ,p0=(1.0,0.2))
            p1_obs = popt[0]
            p2_obs = popt[1]
            yobs2=func24(xax_1hr,p1_obs,p2_obs)+np.mean(obs_data)
            obs2,=plt.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])),np.concatenate((obs_data,obs_data)),'k.',label='OBS: %.2f'%ann_mean,lw=2,markersize=10)
            obs_fit2,=plt.plot(np.concatenate((xax_1hr,[x+24 for x in xax_1hr])), np.concatenate((yobs2,yobs2)),'k',label = 'OBS FFT',lw=2)
            obs2_amp=abs(p1_obs)
            #obs2_phase=0.5*np.pi-p2_obs  #-5.0/24*2*np.pi
            if p1_obs<=0 :
               p2_obs=1.5*np.pi-p2_obs
            if p1_obs>0 :
               p2_obs=0.5*np.pi-p2_obs
            obs2_phase=p2_obs


            #ax.plot(xax_1hr,obs_data[:],'k',label='OBS: %.2f'%ann_mean,lw=3)
            #ann_mean=np.mean(mmm_data[:])
            #ax.plot(xax_3hr,mmm_data[:],'b',label='MMM: %.2f'%ann_mean,lw=3)
            my_xticks=['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h']
            my_xticks_loc=np.array([3*x for x in range(8)])
            plt.xticks(my_xticks_loc, my_xticks)
            ax.set_xlim([0,24])
            #ydn = np.nanmin(cmip_data)
            #yup = np.nanmax(cmip_data)
            #ax.set_ylim([ydn-1,yup+1])
            #ax.text(0.3, 0.95,'OBS',color='k',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)
            #ax.text(0.3, 0.85,'MOD',color='r',verticalalignment='top', horizontalalignment='left',transform=ax.transAxes)
            ax.legend(scatterpoints=1,loc='best',prop={'size':10},framealpha=0.0)
            plt.xlabel('local solar time [hr]')
            plt.ylabel(var_longname[j])
            fig.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_'+season+'_diurnal_cycle_'+sites[0]+'.png')
            plt.close('all')
           
            ##########Generate hormonic dial plot: mapping phase and amplitude to Dial
            hup=3
            if sites[0] == 'twpc1' or sites[0] == 'maom1':
                hup=10
            if sites[0] == 'enac1':
                hup=1

            fig2 = plt.figure()
            ax2  =fig2.add_axes([0.1, 0.1, 0.8, 0.8],polar=True)#, axisbg='#d5de9c')
    
            size=50
            ax2.scatter(obs2_phase,obs2_amp,color='k',label='OBS',s=size*2)
            ax2.scatter(mod_phase[:],abs(mod_amp[:]),color='grey',s=size)
            ax2.scatter(mmm_phase,abs(mmm_amp),color='blue',label='MMM',s=size*2)
            if test_findex == 1: ax2.scatter(test_phase,abs(test_amp),color='r',label='MOD',s=size*2)
            ax2.legend(scatterpoints=1,loc='center right',bbox_to_anchor=(1.2,0.90),prop={'size':10})
            ax2.set_rmax(hup)
            ax2.set_theta_direction(-1)
            ax2.set_theta_offset(np.pi/2)
            ax2.set_xticklabels(['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h'])
            grid(True)
    
            fig2.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_'+season+'_diurnal_cycle_harmonic_diagram_'+sites[0]+'.png')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    


    
    
    
    
