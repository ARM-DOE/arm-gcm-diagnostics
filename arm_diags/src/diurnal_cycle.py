import os
import glob
import cdms2
import cdutil
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from varid_dict import varid_longname
from cdtime import *

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
        t1 = comptime(year,03,01)
        t2 = t1.add(90,Days)
#        try:
        var_yr =  var(time=(t1,t2,'co'))
        var_dc_year[iy,:]= np.nanmean(np.reshape(var_yr,(90,8)), axis=0)
        if var.id == 'tas':
            var_dc_year[iy,:] = var_dc_year[iy,:]-273.15

        if var.id == 'pr':
            var_dc_year[iy,:] = var_dc_year[iy,:]*3600.*24.
        print year
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
    season = parameter.season
   
    test_model = parameter.test_data_set 
    ref_models = parameter.ref_models

    # Calculate for test model
    
#    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*3hr*.nc')) #read in 3hr test data
    fin = cdms2.open(test_file[0])
    
    print 'test_model',test_model

    for j, variable in enumerate(variables): 
        try:
            var = fin (variable,squeeze = 1)
            test_var_dc = var_diurnal_cycle(var,season)
            print test_var_dc

        except:
            print (variable+" not processed for " + test_model)

    # Calculate for observational data
    obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag*diurnal*.nc')) #read in diurnal test data
    print 'ARM data'
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
              
        try:
            var = fin (variable)
            print var.shape
            var_dc = np.reshape(var,(12,24))
            if season == 'JJA':
                obs_var_dc = np.nanmean(var_dc[5:8,:],axis=0)
            if var.id == 'tas':
                obs_var_dc = obs_var_dc-273.15
    
            if var.id == 'pr':
                obs_var_dc = obs_var_dc*3600.*24.
            print obs_var_dc 
        except:
            print (variable+" not processed for obs")

    quit()
    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),8])*np.nan
 
    for i, ref_model in enumerate(ref_models):
         ref_file = glob.glob(os.path.join(cmip_path,'*'+ref_model+'*mo*.nc')) #read in monthly cmip data
         print 'ref_model', ref_model
         if not ref_file :
             print (ref_model+" not found!") 
         else:
             fin = cdms2.open(ref_file[0])
         
             for j, variable in enumerate(variables): 
                 try:
                     var = fin (variable)
                     cmip_var_season[i, j, :] = var_diurnal_cycle(var, seasons)

                 except:
                     print (variable+" not processed for " + ref_model)
             fin.close()  
    # Calculate multi-model mean
    mmm_var_season =  np.nanmean(cmip_var_season,axis=0)

    # Save data in csv format in metrics folder
    for j, variable in enumerate(variables):
        np.savetxt(output_path+'/metrics/'+variable+'_test_diurnal_cycle.csv',test_var_season[j,:])
        np.savetxt(output_path+'/metrics/'+variable+'_mmm_diurnal_cycle.csv',mmm_var_season[j,:])
        np.savetxt(output_path+'/metrics/'+variable+'_cmip_diurnal_cycle.csv',cmip_var_season[:,j,:])
        np.savetxt(output_path+'/metrics/'+variable+'_obs_diurnal_cycle.csv',obs_var_season[j,:])

        # Reference dapret
        data = obs_var_season[j,:]
        refstd = data.std(ddof=1)           # Reference standard deviation
        x=np.arange(len(seasons))

        # Compute and save stddev and correlation coefficient of models,for taylor diagram
        mod_num=len(ref_models)
        m_all=[cmip_var_season[x,j,:] for x in range(mod_num)]
        cmip_samples = np.array([ [m.std(ddof=1), np.corrcoef(data, m)[0,1]] for m in m_all])
        test_sample=np.array([test_var_season[j,:].std(ddof=1), np.corrcoef(data, test_var_season[j,:])[0,1]])
        mmm_sample=np.array([mmm_var_season[j,:].std(ddof=1), np.corrcoef(data,mmm_var_season[j,:])[0,1]])
        obs_sample=np.array([refstd,1.0])
        np.savetxt(output_path+'/metrics/'+variable+'_obs_diurnal_cycle_std_corr.csv',obs_sample)
        np.savetxt(output_path+'/metrics/'+variable+'_test_diurnal_cycle_std_corr.csv',test_sample)
        np.savetxt(output_path+'/metrics/'+variable+'_mmm_diurnal_cycle_std_corr.csv',mmm_sample)
        np.savetxt(output_path+'/metrics/'+variable+'_cmip_diurnal_cycle_std_corr.csv',cmip_samples)
    

def diurnal_cycle_line_plot(parameter):
    """Calculate diurnal cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path

    var_longname = [ varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        test_data = genfromtxt(output_path+'/metrics/'+variable+'_test_diurnal_cycle.csv')
        mmm_data = genfromtxt(output_path+'/metrics/'+variable+'_mmm_diurnal_cycle.csv')
        obs_data = genfromtxt(output_path+'/metrics/'+variable+'_obs_diurnal_cycle.csv')
        cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_cmip_diurnal_cycle.csv')
        mod_num = cmip_data.shape[0]

        fig = plt.figure()# Create figure
        ax  =fig.add_axes([0.15, 0.14, 0.8, 0.8]) # Create axes
        xax =  np.arange (1,13,1)

        for mod_ind in range(mod_num):
            ax.plot(xax,cmip_data[mod_ind,:],'grey',lw=1)
        ann_mean=np.mean(test_data[:])
        ax.plot(xax,test_data[:],'r',label='MOD: %.2f'%ann_mean,lw=3)
        ann_mean=np.mean(obs_data[:])
        ax.plot(xax,obs_data[:],'k',label='OBS: %.2f'%ann_mean,lw=3)
        ann_mean=np.mean(mmm_data[:])
        ax.plot(xax,mmm_data[:],'b',label='MMM: %.2f'%ann_mean,lw=3)
        #my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
        my_xticks = seasons
        plt.xticks(xax, my_xticks)
        plt.xlim(1,12)
#        plt.ylim(ylim[va_ind])
        plt.title('Annual Cycle: Model vs OBS vs CMIP' )
        plt.xlabel('Month')
        plt.legend(loc='best',prop={'size':15})
        plt.ylabel(var_longname[j])
        fig.savefig(output_path+'/figures/'+variable+'_diurnal_cycle.png')
        plt.close('all')
       

    
def diurnal_cycle_taylor_diagram(parameter):
    """Calculate diurnal cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path

    var_longname = [ varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        obs_data = genfromtxt(output_path+'/metrics/'+variable+'_obs_diurnal_cycle_std_corr.csv')
        test_data = genfromtxt(output_path+'/metrics/'+variable+'_test_diurnal_cycle_std_corr.csv')
        mmm_data = genfromtxt(output_path+'/metrics/'+variable+'_mmm_diurnal_cycle_std_corr.csv')
        cmip_data = genfromtxt(output_path+'/metrics/'+variable+'_cmip_diurnal_cycle_std_corr.csv')
        mod_num = cmip_data.shape[0]
        

        fig = plt.figure(figsize=(8,8))
        refstd = obs_data[0]
        dia = TaylorDiagram(refstd, fig=fig,rect=111, label="Reference")

        # Add samples to Taylor diagram
        for i,(stddev,corrcoef) in enumerate(cmip_data):
            dia.add_sample(stddev, corrcoef, marker='.',ms=10, c='grey')

        dia.add_sample(test_data[0], test_data[1],marker='.',ms=15, c='red',label='MOD')
        dia.add_sample(mmm_data[0], mmm_data[1],marker='.',ms=15, c='b',label='MMM')

        # Add RMS contours, and label them
        contours = dia.add_contours(colors='0.5')
        plt.clabel(contours, inline=1, fontsize=10)
        plt.title(var_longname[j])

        # Add a figure legend
        fig.legend([dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]] ,
                   [ p.get_label() for p in [dia.samplePoints[0],dia.samplePoints[-2],dia.samplePoints[-1]] ],
                   numpoints=1,  loc='upper right',prop={'size':10})
#        np.savetxt(basedir+'metrics/'+vas[va_ind]+'_'+mod+'std_corr.csv',mod_sample,fmt='%.3f')
        fig.savefig(output_path+'/figures/'+variable+'_diurnal_cycle_taylor_diagram.png')
        plt.close('all')


    
    
    
    
