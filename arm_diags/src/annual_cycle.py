#===========================================================================================================================
# Program for generate annual/seasonal cycle & line plot from monthly data -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### suppress the taylor diagram and output note, when observation annual mean is not valid
    # ### change the input/output format to site-dependent
    # ### minor fix on the plotting code for better visualization
    # ----------------------------------------------------------------------------------------------------

#===========================================================================================================================
import os
import pdb
import glob
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
import xarray as xr
import xcdat
from .varid_dict import varid_longname
from .taylor_diagram import TaylorDiagram
from .utils import climo
from .data_utils import open_dataset, annual_cycle_climatology

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def var_annual_cycle(var, seasons):
    """
    Calculate annual cycle climatology of each variable
    
    Args:
        var: xarray.DataArray
        seasons: List of seasons
        
    Returns:
        Monthly climatology data
    """
    # Ensure we're working with an xarray DataArray
    if not isinstance(var, xr.DataArray):
        if hasattr(var, 'getValue'):
            # Convert from cdms2 format
            # Create a DataArray with proper attributes
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
    
    # Use xcdat for temporal operations
    da_xcdat = xcdat.Dataset({"var": da}).var
    var_season_data = da_xcdat.temporal.climatology(freq="month")
    
    # Convert units
    var_id = getattr(var, 'id', getattr(da, 'name', None))
    if var_id == 'tas':
        var_season_data = var_season_data - 273.15
    
    if var_id == 'pr':
        var_season_data = var_season_data * 3600.0 * 24.0
    
    return var_season_data

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_data(parameter):
    """
    Calculate annual cycle climatology using xarray/xcdat
    
    Args:
        parameter: Parameter object with configuration settings
    """
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
    print('Create Annual Cycles: '+sites[0])
    print('============================================================')

    # Calculate for test model
    test_var_season=np.empty([len(variables),len(seasons)])*np.nan
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path,'*'+test_model+'*mo*' + sites[0]+'.nc' )) #read in monthly test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        print(test_path,test_model,sites[0][:3]+test_model+'mon' + sites[0][3:5].upper())
        test_file = glob.glob(os.path.join(test_path,sites[0][:3]+test_model+'mon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data

    print('test_file',test_file)
        
    if len(test_file) == 0:
       raise RuntimeError('No monthly data for test model were found.')

    # Open test data with xarray
    test_ds = open_dataset(test_file[0])
    
    print(('test_model',test_model))

    for j, variable in enumerate(variables): 
        try:
            # Extract variable from dataset
            if variable in test_ds:
                var = test_ds[variable]
            else:
                # Try case-insensitive matching
                var_found = False
                for test_var in test_ds.data_vars:
                    if test_var.lower() == variable.lower():
                        var = test_ds[test_var]
                        var.attrs['id'] = variable
                        var_found = True
                        break
                if not var_found:
                    print(f"{variable} not found in test dataset")
                    continue
                    
            # Calculate climatology
            test_var_season[j, :] = climo(var, 'ANNUALCYCLE')
            print(('after', test_var_season[j, :]))

        except Exception as e:
            print(f"{variable} not processed for {test_model}: {e}")
    
    # Close dataset if needed
    test_ds.close()

    # Calculate for observational data
    obs_var_season=np.empty([len(variables),len(seasons)])*np.nan
    print('ARM data',sites[0])
    # read in the monthly data for target site, format unified [XZ]
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path,'*ARMdiag*monthly_climo*'+ sites[0]+'.nc')) #read in monthly data
    else:
        obs_file = glob.glob(os.path.join(obs_path,sites[0][:3]+'armdiagsmon' + sites[0][3:5].upper()+'*c1.nc')) #read in monthly data
    print('obs_file',obs_file)
    
    # Open observation data with xarray
    obs_ds = open_dataset(obs_file[0])
    
    for j, variable in enumerate(variables): 
        try:
            # Extract variable from dataset
            if variable in obs_ds:
                var = obs_ds[variable]
            else:
                # Try case-insensitive matching
                var_found = False
                for obs_var in obs_ds.data_vars:
                    if obs_var.lower() == variable.lower():
                        var = obs_ds[obs_var]
                        var.attrs['id'] = variable
                        var_found = True
                        break
                if not var_found:
                    print(f"{variable} not found in observation dataset")
                    continue
                    
            # Calculate climatology
            obs_var_season[j, :] = climo(var, 'ANNUALCYCLE')

        except Exception as e:
            print(f"{variable} not processed for obs: {e}")
    
    # Close dataset if needed
    obs_ds.close()
  
    # Calculate cmip model seasonal mean climatology
    cmip_var_season=np.empty([len(ref_models),len(variables),len(seasons)])*np.nan
 
    for i, ref_model in enumerate(ref_models):
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path,'*'+ref_model+'*mo*'+ sites[0]+'.nc')) #read in monthly cmip data
        else:
            ref_model = cmip_ver +''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path,sites[0]+'/'+sites[0][:3]+ref_model+'mon' + sites[0][3:5].upper()+'*.nc' )) #read in monthly test data
            print('ref_file',ref_file, ref_model,sites[0][:3]+ref_model+'mon' + sites[0][3:5].upper())
        print(('ref_model', ref_model))
        
        if not ref_file:
            print(f"{ref_model} not found!")
        else:
            # Open reference model data with xarray
            ref_ds = open_dataset(ref_file[0])
            
            for j, variable in enumerate(variables): 
                try:
                    # Extract variable from dataset
                    if variable in ref_ds:
                        var = ref_ds[variable]
                    else:
                        # Try case-insensitive matching
                        var_found = False
                        for ref_var in ref_ds.data_vars:
                            if ref_var.lower() == variable.lower():
                                var = ref_ds[ref_var]
                                var.attrs['id'] = variable
                                var_found = True
                                break
                        if not var_found:
                            print(f"{variable} not found in {ref_model} dataset")
                            continue
                            
                    # Calculate climatology
                    tmpvarannual = climo(var, 'ANNUALCYCLE')
                    
                    # Check for invalid data
                    lnn = np.where(tmpvarannual == 0)[0]
                    if len(lnn) == 12: 
                        tmpvarannual[:] = np.nan  # Set to missing if model output is invalid
                    
                    cmip_var_season[i, j, :] = tmpvarannual.copy()
                    print((ref_model, cmip_var_season[i, j, :]))

                except Exception as e:
                    print(f"{variable} not processed for {ref_model}: {e}")
            
            # Close dataset if needed
            ref_ds.close()
            
    # Calculate multi-model mean
    mmm_var_season = np.nanmean(cmip_var_season, axis=0)

    # Save data in csv format in metrics folder
    # Generate new folder given site names [XZ]:
    if not os.path.exists(os.path.join(output_path,'metrics',sites[0])):
        os.makedirs(os.path.join(output_path,'metrics',sites[0])) 
    
    for j, variable in enumerate(variables):
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_'+sites[0]+'.csv',test_var_season[j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_'+sites[0]+'.csv',mmm_var_season[j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_'+sites[0]+'.csv',cmip_var_season[:,j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv',obs_var_season[j,:])

        # Reference data preparation
        data = obs_var_season[j,:]
        refstd = data.std(ddof=1)  # Reference standard deviation
        x=np.arange(len(seasons))

        # Compute and save stddev and correlation coefficient of models, for taylor diagram
        mod_num=len(ref_models)
        m_all=[cmip_var_season[x,j,:] for x in range(mod_num)]
        cmip_samples = np.array([[m.std(ddof=1), np.corrcoef(data, m)[0,1]] for m in m_all])
        test_sample=np.array([test_var_season[j,:].std(ddof=1), np.corrcoef(data, test_var_season[j,:])[0,1]])
        mmm_sample=np.array([mmm_var_season[j,:].std(ddof=1), np.corrcoef(data,mmm_var_season[j,:])[0,1]])
        obs_sample=np.array([refstd,1.0])
        
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_std_corr_'+sites[0]+'.csv',obs_sample)
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_std_corr_'+sites[0]+'.csv',test_sample)
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_std_corr_'+sites[0]+'.csv',mmm_sample)
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_std_corr_'+sites[0]+'.csv',cmip_samples)
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_line_plot(parameter):
    """Calculate annual cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    var_longname = [ varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        test_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_'+sites[0]+'.csv')
        mmm_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_'+sites[0]+'.csv')
        obs_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv')
        cmip_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_'+sites[0]+'.csv')
        mod_num = cmip_data.shape[0]

        fig = plt.figure()# Create figure
        ax  =fig.add_axes([0.12, 0.12, 0.82, 0.81]) # Create axes
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
        plt.title('Annual Cycle: Model vs OBS vs CMIP',fontsize=15)
        plt.xlabel('Month',fontsize=15)
        plt.legend(loc='best',prop={'size':12})
        plt.ylabel(var_longname[j])
        #special notes for models mistreating surface type [XZ]:
        if (variable == 'hfls') or (variable == 'hfss') or (variable == 'rsus'):
            if (sites[0] == 'enac1') or (sites[0] == 'twpc1') or (sites[0] == 'twpc2') or (sites[0] == 'twpc3'):
                ax.text(0.5, 0.05,'Note: the selected grid points were ocean grids in most GCMs', ha='center', va='center', transform=ax.transAxes,fontsize=8)
        # save figures
        fig.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_annual_cycle_'+sites[0]+'.png')
        plt.close('all')
       
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_taylor_diagram(parameter):
    """Calculate annual cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    var_longname = [ varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        obs_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_std_corr_'+sites[0]+'.csv')
        test_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_std_corr_'+sites[0]+'.csv')
        mmm_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_std_corr_'+sites[0]+'.csv')
        cmip_data = genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_std_corr_'+sites[0]+'.csv')
        mod_num = cmip_data.shape[0]
        # observational annual mean must be valid for taylor diagram [XZ]
        if np.isfinite(obs_data[0]):
            try:
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
#                np.savetxt(basedir+'metrics/'+vas[va_ind]+'_'+mod+'std_corr.csv',mod_sample,fmt='%.3f')
                fig.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_annual_cycle_taylor_diagram_'+sites[0]+'.png')
                plt.close('all')
            except:    
                print(('Taylor diagram not generated for ' +variable+': plotting error'))
        else:
            print(('Taylor diagram not generated for ' +variable+': observation annual mean not valid'))
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
    
    
