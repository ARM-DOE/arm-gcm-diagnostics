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
import numpy as np
import xarray as xr
import pandas as pd
import csv
from .varid_dict import varid_longname
from .core import climo
from .dataset import open_dataset

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def var_seasons(var, seasons):
    """
    Calculate seasonal climatology of each variable using xarray/xcdat
    
    Args:
        var: xarray.DataArray with time dimension
        seasons: List of season names
        
    Returns:
        numpy array of seasonal climatologies
    """
    var_season_data = np.empty([len(seasons)]) * np.nan
    
    # Convert to xarray DataArray if it's not already
    if not isinstance(var, xr.DataArray):
        # Convert from cdms2 format (for backward compatibility)
        if hasattr(var, 'getValue'):
            values = var.getValue()
            var_id = getattr(var, 'id', 'unknown')
            da = xr.DataArray(values, name=var_id)
            da.attrs['id'] = var_id
        else:
            # It's a numpy array or similar
            values = np.array(var)
            da = xr.DataArray(values)
    else:
        da = var
    
    # Process each season
    for k, season in enumerate(seasons):
        var_season_data[k] = climo(da, season)
    
    # Convert units
    var_id = getattr(var, 'id', getattr(da, 'name', None))
    if var_id == 'tas':
        var_season_data = var_season_data - 273.15
    
    if var_id == 'pr':
        var_season_data = var_season_data * 3600.0 * 24.0
       
        
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
 
    # Open test data with Dataset class
    test_dataset = open_dataset(test_file[0], name=test_model)
    
    print(('test_model',test_model))

    for j, variable in enumerate(variables): 
        try:
            # Get variable from dataset
            var = test_dataset.get_variable(variable)
            #test_var_season[j, :] = var_seasons(var, seasons)
            test_var_season[j, :] = climo(var, seasons)

        except Exception as e:
            print(f"{variable} not processed for {test_model}: {e}")
    
    # Close dataset
    test_dataset.close()

    # Calculate for observational data
    # read in the monthly data for target site, format unified [XZ]
    obs_var_season=np.empty([len(variables),len(seasons)])*np.nan
    print('ARM data',sites[0])
        
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path,'ARMdiag*monthly_climo*'+ sites[0]+'.nc')) #read in monthly test data
    else:
        obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsmon' + sites[0][3:5].upper()+'*c1.nc')) #read in monthly test data
    print('obs_file',obs_file)
    
    # Open observation data with Dataset class
    obs_dataset = open_dataset(obs_file[0], name="OBS")
    
    for j, variable in enumerate(variables): 
        try:
            # Get variable from dataset
            var = obs_dataset.get_variable(variable)
            obs_var_season[j, :] = climo(var, seasons)
    
        except Exception as e:
            print(f"{variable} not processed for obs: {e}")
    
    # Close dataset
    obs_dataset.close()
   
  
    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),len(seasons)])*np.nan
 
    for i, ref_model in enumerate(ref_models):
         if not arm_name:
             ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+'*'+ref_model+'*mo*'+ sites[0]+'.nc')) #read in monthly cmip data
         else:
             ref_model = cmip_ver +''.join(e for e in ref_model if e.isalnum()).lower()
             ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+sites[0][:3]+ref_model+'mon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data
         print(('ref_model', ref_model))
         if not ref_file:
             print(f"{ref_model} not found!") 
         else:
             # Open reference model data with Dataset class
             ref_dataset = open_dataset(ref_file[0], name=ref_model)
         
             for j, variable in enumerate(variables): 
                 try:
                     # Get variable from dataset
                     var = ref_dataset.get_variable(variable)
                     #cmip_var_season[i, j, :] = var_seasons(var, seasons)
                     cmip_var_season[i, j, :] = climo(var, seasons)

                 except Exception as e:
                     print(f"{variable} not processed for {ref_model}: {e}")
             
             # Close dataset
             ref_dataset.close()  
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
    
    
    
    
    
