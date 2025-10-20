#===========================================================================================================================
# Program for generate annual/seasonal cycle & line plot from monthly data
#---------------------------------------------------------------------------------------------------------------------------
# V4 Development
    # ----------------------------------------------------------------------------------------------------
    # Refactored to use xarray instead of cdms2
    # Maintained original functionality while modernizing the code
    # ----------------------------------------------------------------------------------------------------

#===========================================================================================================================
import os
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from .varid_dict import varid_longname
from .taylor_diagram import TaylorDiagram

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def convert_units(da):
    """Convert units for common variables."""
    if da.name == 'tas':
        # Convert K to C if needed
        if hasattr(da, 'units') and da.units == 'K':
            da = da - 273.15
            da.attrs['units'] = 'C'
    
    if da.name == 'pr':
        # Convert kg m-2 s-1 to mm/day if needed
        if hasattr(da, 'units') and ('kg' in da.units or 's-1' in da.units):
            da = da * 3600.0 * 24.0
            da.attrs['units'] = 'mm/day'
    
    return da

def var_annual_cycle(ds, var_name, seasons=None):
    """Calculate annual cycle climatology of each variable using xarray."""
    if var_name not in ds:
        print(f"Variable {var_name} not found in dataset")
        return np.full(12, np.nan)
    
    # Extract the variable
    da = ds[var_name]
    
    # Calculate monthly climatology (group by month and average)
    with xr.set_options(keep_attrs=True):
        monthly_clim = da.groupby('time.month').mean(dim='time')
    
    # Apply unit conversions
    monthly_clim = convert_units(monthly_clim)
    
    # Convert to numpy array (maintaining the original function's return type)
    return monthly_clim.values

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_data(parameter):
    """Calculate annual cycle climatology using xarray."""
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
    test_var_season = np.empty([len(variables), len(seasons)]) * np.nan
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path, '*'+test_model+'*mo*' + sites[0]+'.nc'))
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        print(test_path, test_model, sites[0][:3]+test_model+'mon' + sites[0][3:5].upper())
        test_file = glob.glob(os.path.join(test_path, sites[0][:3]+test_model+'mon' + sites[0][3:5].upper()+'*.nc'))

    print('test_file', test_file)
        
    if len(test_file) == 0:
       raise RuntimeError('No monthly data for test model were found.')

    # Open dataset with xarray
    test_ds = xr.open_dataset(test_file[0])
    print('test_model', test_model)

    for j, variable in enumerate(variables): 
        try:
            test_var_season[j, :] = var_annual_cycle(test_ds, variable, seasons)
            print('after', test_var_season[j, :])
        except Exception as e:
            print(f"{variable} not processed for {test_model}: {e}")
    
    # Close the dataset
    test_ds.close()

    # Calculate for observational data
    obs_var_season = np.empty([len(variables), len(seasons)]) * np.nan
    print('ARM data', sites[0])
    # Read in the monthly data for target site, format unified
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path, '*ARMdiag*monthly_climo*'+ sites[0]+'.nc'))
    else:
        obs_file = glob.glob(os.path.join(obs_path, sites[0][:3]+'armdiagsmon' + sites[0][3:5].upper()+'*c1.nc'))
    
    print('obs_file', obs_file)
    
    if len(obs_file) == 0:
        print(f"No observational data found for {sites[0]}")
    else:
        # Open dataset with xarray
        obs_ds = xr.open_dataset(obs_file[0])
        
        for j, variable in enumerate(variables): 
            try:
                obs_var_season[j, :] = var_annual_cycle(obs_ds, variable, seasons)
            except Exception as e:
                print(f"{variable} not processed for obs: {e}")
        
        # Close the dataset
        obs_ds.close()
  
    # Calculate cmip model seasonal mean climatology
    cmip_var_season = np.empty([len(ref_models), len(variables), len(seasons)]) * np.nan
 
    for i, ref_model in enumerate(ref_models):
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path, '*'+ref_model+'*mo*'+ sites[0]+'.nc'))
        else:
            ref_model_name = cmip_ver +''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path, sites[0]+'/'+ sites[0][:3]+ref_model_name+'mon' + sites[0][3:5].upper()+'*.nc'))
            print('ref_file', ref_file, ref_model, sites[0][:3]+ref_model_name+'mon' + sites[0][3:5].upper())
        
        print('ref_model', ref_model)
        
        if not ref_file:
            print(f"{ref_model} not found!")
        else:
            # Open dataset with xarray
            ref_ds = xr.open_dataset(ref_file[0])
            
            for j, variable in enumerate(variables): 
                try:
                    tmpvarannual = var_annual_cycle(ref_ds, variable, seasons)
                    # Check for invalid data (all zeros)
                    if np.all(tmpvarannual == 0):
                        tmpvarannual = np.full_like(tmpvarannual, np.nan)
                    cmip_var_season[i, j, :] = tmpvarannual
                    print(ref_model, cmip_var_season[i, j, :])
                except Exception as e:
                    print(f"{variable} not processed for {ref_model}: {e}")
            
            # Close the dataset
            ref_ds.close()  
    
    # Calculate multi-model mean
    mmm_var_season = np.nanmean(cmip_var_season, axis=0)

    # Save data in csv format in metrics folder
    # Generate new folder given site names
    if not os.path.exists(os.path.join(output_path, 'metrics', sites[0])):
        os.makedirs(os.path.join(output_path, 'metrics', sites[0])) 
    
    for j, variable in enumerate(variables):
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_'+sites[0]+'.csv', test_var_season[j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_'+sites[0]+'.csv', mmm_var_season[j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_'+sites[0]+'.csv', cmip_var_season[:,j,:])
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv', obs_var_season[j,:])

        # Reference for Taylor diagram
        data = obs_var_season[j,:]
        refstd = np.nanstd(data, ddof=1)  # Reference standard deviation
        x = np.arange(len(seasons))

        # Compute and save stddev and correlation coefficient of models for taylor diagram
        mod_num = len(ref_models)
        m_all = [cmip_var_season[x,j,:] for x in range(mod_num)]
        
        # Calculate statistics, handling NaN values
        cmip_samples = np.array([
            [np.nanstd(m, ddof=1), 
             np.corrcoef(data[~np.isnan(data) & ~np.isnan(m)], 
                         m[~np.isnan(data) & ~np.isnan(m)])[0,1] 
             if len(data[~np.isnan(data) & ~np.isnan(m)]) > 1 else np.nan]
            for m in m_all
        ])
        
        # Test model stats
        test_sample = np.array([
            np.nanstd(test_var_season[j,:], ddof=1),
            np.corrcoef(data[~np.isnan(data) & ~np.isnan(test_var_season[j,:])], 
                        test_var_season[j,:][~np.isnan(data) & ~np.isnan(test_var_season[j,:])])[0,1]
            if len(data[~np.isnan(data) & ~np.isnan(test_var_season[j,:])]) > 1 else np.nan
        ])
        
        # Multi-model mean stats
        mmm_sample = np.array([
            np.nanstd(mmm_var_season[j,:], ddof=1),
            np.corrcoef(data[~np.isnan(data) & ~np.isnan(mmm_var_season[j,:])], 
                        mmm_var_season[j,:][~np.isnan(data) & ~np.isnan(mmm_var_season[j,:])])[0,1]
            if len(data[~np.isnan(data) & ~np.isnan(mmm_var_season[j,:])]) > 1 else np.nan
        ])
        
        obs_sample = np.array([refstd, 1.0])
        
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_std_corr_'+sites[0]+'.csv', obs_sample)
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_std_corr_'+sites[0]+'.csv', test_sample)
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_std_corr_'+sites[0]+'.csv', mmm_sample)
        np.savetxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_std_corr_'+sites[0]+'.csv', cmip_samples)
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_line_plot(parameter):
    """Calculate annual cycle climatology"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites

    if not os.path.exists(os.path.join(output_path,'figures',sites[0])):
        os.makedirs(os.path.join(output_path,'figures',sites[0])) 

    var_longname = [varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        test_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_'+sites[0]+'.csv')
        mmm_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_'+sites[0]+'.csv')
        obs_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_'+sites[0]+'.csv')
        cmip_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_'+sites[0]+'.csv')
        mod_num = cmip_data.shape[0]

        fig = plt.figure()# Create figure
        ax = fig.add_axes([0.12, 0.12, 0.82, 0.81]) # Create axes
        xax = np.arange(1, 13, 1)

        for mod_ind in range(mod_num):
            ax.plot(xax, cmip_data[mod_ind,:], 'grey', lw=1)
        
        ann_mean = np.nanmean(test_data[:])
        ax.plot(xax, test_data[:], 'r', label='MOD: %.2f'%ann_mean, lw=3)
        
        ann_mean = np.nanmean(obs_data[:])
        ax.plot(xax, obs_data[:], 'k', label='OBS: %.2f'%ann_mean, lw=3)
        
        ann_mean = np.nanmean(mmm_data[:])
        ax.plot(xax, mmm_data[:], 'b', label='MMM: %.2f'%ann_mean, lw=3)
        
        my_xticks = seasons
        plt.xticks(xax, my_xticks)
        plt.xlim(1, 12)
        plt.title('Annual Cycle: Model vs OBS vs CMIP', fontsize=15)
        plt.xlabel('Month', fontsize=15)
        plt.legend(loc='best', prop={'size': 12})
        plt.ylabel(var_longname[j])
        
        # Special notes for models mistreating surface type
        if (variable == 'hfls') or (variable == 'hfss') or (variable == 'rsus'):
            if (sites[0] == 'enac1') or (sites[0] == 'twpc1') or (sites[0] == 'twpc2') or (sites[0] == 'twpc3'):
                ax.text(0.5, 0.05, 'Note: the selected grid points were ocean grids in most GCMs', 
                        ha='center', va='center', transform=ax.transAxes, fontsize=8)
        
        # Save figures
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

    var_longname = [varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        obs_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_obs_annual_cycle_std_corr_'+sites[0]+'.csv')
        test_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_test_annual_cycle_std_corr_'+sites[0]+'.csv')
        mmm_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_mmm_annual_cycle_std_corr_'+sites[0]+'.csv')
        cmip_data = np.genfromtxt(output_path+'/metrics/'+sites[0]+'/'+variable+'_cmip_annual_cycle_std_corr_'+sites[0]+'.csv')
        mod_num = cmip_data.shape[0]
        
        # Observational annual mean must be valid for taylor diagram
        if np.isfinite(obs_data[0]):
            try:
                fig = plt.figure(figsize=(8, 8))
                refstd = obs_data[0]
                dia = TaylorDiagram(refstd, fig=fig, rect=111, label="Reference")

                # Add samples to Taylor diagram
                for i, (stddev, corrcoef) in enumerate(cmip_data):
                    if np.isfinite(stddev) and np.isfinite(corrcoef):
                        dia.add_sample(stddev, corrcoef, marker='.', ms=10, c='grey')

                # Add test model and multi-model mean if valid
                if np.isfinite(test_data[0]) and np.isfinite(test_data[1]):
                    dia.add_sample(test_data[0], test_data[1], marker='.', ms=15, c='red', label='MOD')
                
                if np.isfinite(mmm_data[0]) and np.isfinite(mmm_data[1]):
                    dia.add_sample(mmm_data[0], mmm_data[1], marker='.', ms=15, c='b', label='MMM')

                # Add RMS contours, and label them
                contours = dia.add_contours(colors='0.5')
                plt.clabel(contours, inline=1, fontsize=10)
                plt.title(var_longname[j])

                # Add a figure legend
                fig.legend([dia.samplePoints[0], dia.samplePoints[-2], dia.samplePoints[-1]],
                           [p.get_label() for p in [dia.samplePoints[0], dia.samplePoints[-2], dia.samplePoints[-1]]],
                           numpoints=1, loc='upper right', prop={'size': 10})
                
                fig.savefig(output_path+'/figures/'+sites[0]+'/'+variable+'_annual_cycle_taylor_diagram_'+sites[0]+'.png')
                plt.close('all')
            except Exception as e:    
                print(f'Taylor diagram not generated for {variable}: plotting error - {e}')
        else:
            print(f'Taylor diagram not generated for {variable}: observation annual mean not valid')
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
    
    