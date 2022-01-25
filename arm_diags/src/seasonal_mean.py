#===========================================================================================================================
# Program for generate annual/seasonal table from monthly data -- Originally written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### change the input/output format to site-dependent
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================

import os
import pdb
import glob
import cdms2
import cdutil
import numpy as np
import csv
from .varid_dict import varid_longname
from .utils import climo

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def var_seasons(var, seasons):
    "Calculate seasonal climatology of each variable"
    var_season_data = np.empty([len(seasons)])*np.nan
    cdutil.setTimeBoundsMonthly(var)
    for k, season in enumerate(seasons):
        if season == 'ANN':
            months = cdutil.times.Seasons('DJFMAMJJASON')
        else:
            months = cdutil.times.Seasons(str(season))
        var_season_data[k] = months.climatology(var)
    # convert units
    if var.id == 'tas':
        var_season_data = var_season_data-273.15

    if var.id == 'pr':
        var_season_data = var_season_data*3600.*24.
       
        
    return var_season_data

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def seasonal_mean_table(parameter):
    """Calculate seasonal mean climatology"""
    variables = parameter.variables
    seasons = parameter.season
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites
   
    test_model = parameter.test_data_set 
    ref_models = parameter.ref_models

    arm_name = parameter.arm_filename

    cmip_ver = cmip_path.split('/')[-1]

    print('============================================================')
    print('Create Seasonal Mean Tables: '+sites[0])
    print('============================================================')

    # Calculate for test model
    test_var_season=np.empty([len(variables),len(seasons)])*np.nan

    if not arm_name:
        test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*mo*'+ sites[0]+'.nc')) #read in monthly test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'mon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data
    print('test_file',test_file)

    if len(test_file) == 0:
       raise RuntimeError('No monthly data for test model were found.')
 
    fin = cdms2.open(test_file[0])
    
    print(('test_model',test_model))

    for j, variable in enumerate(variables): 
        try:
            var = fin(variable)
            #test_var_season[j, :] = var_seasons(var, seasons)
            test_var_season[j, :] = climo(var, seasons)

        except:
            print((variable+" not processed for " + test_model))
    fin.close()

    # Calculate for observational data
    # read in the monthly data for target site, format unified [XZ]
    obs_var_season=np.empty([len(variables),len(seasons)])*np.nan
    print('ARM data',sites[0])
        
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path,'ARMdiag*monthly_climo*'+ sites[0]+'.nc')) #read in monthly test data
    else:
        obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsmon' + sites[0][3:5].upper()+'*c1.nc')) #read in monthly test data
    print('obs_file',obs_file)
    fin = cdms2.open(obs_file[0])
    for j, variable in enumerate(variables): 
        try:
            var = fin (variable)
            obs_var_season[j, :] = climo(var, seasons)
    
        except:
            print((variable+" not processed for obs"))
    fin.close()
   
  
    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),len(seasons)])*np.nan
 
    for i, ref_model in enumerate(ref_models):
         if not arm_name:
             ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+'*'+ref_model+'*mo*'+ sites[0]+'.nc')) #read in monthly cmip data
         else:
             ref_model = cmip_ver +''.join(e for e in ref_model if e.isalnum()).lower()
             ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+sites[0][:3]+ref_model+'mon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data
         print(('ref_model', ref_model))
         if not ref_file :
             print((ref_model+" not found!")) 
         else:
             fin = cdms2.open(ref_file[0])
         
             for j, variable in enumerate(variables): 
                 try:
                     var = fin (variable)
                     #cmip_var_season[i, j, :] = var_seasons(var, seasons)
                     cmip_var_season[i, j, :] = climo(var, seasons)

                 except:
                     print((variable+" not processed for " + ref_model))
             fin.close()  
    # Calculate multi-model mean
    mmm_var_season =  np.nanmean(cmip_var_season,axis=0)
    
    # Save data as a table
    #header=['Variables','Model','Obs','Model-Obs','CMIP5','RMSE']
    header=['Variables','Model','Obs','Model-Obs',cmip_path.split('/')[-1].upper()]
    var_longname = [ varid_longname[x] for x in variables]
    table_data = np.empty([len(variables),len(seasons),4])

    for k, season in enumerate(seasons):
        for j, variable in enumerate(variables):
            table_data[j,k,:] = (round(test_var_season[j,k],3), round(obs_var_season[j,k],3),round(test_var_season[j,k]-obs_var_season[j,k],3),round(mmm_var_season[j,k],3))

        # Generate new folder given site names [XZ]:
        if not os.path.exists(os.path.join(output_path,'metrics',sites[0])):
            os.makedirs(os.path.join(output_path,'metrics',sites[0]))           
        with open(output_path+'/metrics/'+sites[0]+'/'+'seasonal_mean_table_'+season+'_'+sites[0]+'.csv','w') as f1:
            writer=csv.writer(f1, delimiter=',',lineterminator='\n', quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            #use tuple to generate csv 
            writer.writerows([c]+row.tolist() for c, row in zip(var_longname,table_data[:,k,:]))

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    
    
    
    
