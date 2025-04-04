#===========================================================================================================================
# Program for generate annual/seasonal cycle & line plot from monthly data
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Aug2022
    # ### modification based on annual_cycle.pro to accommodate the aci annual cycle metrics
    # ----------------------------------------------------------------------------------------------------
# V4 Development
    # ----------------------------------------------------------------------------------------------------
    # Refactored to use xarray instead of cdms2/cdutil
    # Maintained original functionality while modernizing the code
    # ----------------------------------------------------------------------------------------------------

#===========================================================================================================================
import os
import glob
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from .varid_dict import varid_longname
from .taylor_diagram import TaylorDiagram
import xarray as xr

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

def calculate_annual_cycle(da):
    """
    Calculate annual cycle climatology of each variable using xarray.
    
    Parameters
    ----------
    da : xarray.DataArray
        DataArray containing the variable data
        
    Returns
    -------
    np.ndarray
        Array of monthly mean values
    """
    # Apply unit conversions
    da = convert_units(da)
    
    # Calculate monthly climatology
    try:
        # Group by month and calculate mean
        monthly_clim = da.groupby('time.month').mean(dim='time')
        
        # Convert to numpy array and ensure correct order (1-12)
        months = np.arange(1, 13)
        result = np.empty(12)
        
        for i, month in enumerate(months):
            if month in monthly_clim.month.values:
                result[i] = float(monthly_clim.sel(month=month).values)
            else:
                result[i] = np.nan
                
        return result
        
    except Exception as e:
        print(f"Error calculating annual cycle: {e}")
        return np.full(12, np.nan)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_aci_data(parameter):
    """Calculate annual cycle climatology using xarray"""
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

    # Control flags for test and CMIP data availability
    test_index = 0
    cmip_index = 0
    
    print('============================================================')
    print(f'Create Annual Cycles: {sites[0]}')
    print('============================================================')

    # Create output directory if it doesn't exist
    if not os.path.exists(os.path.join(output_path, 'metrics', sites[0])):
        os.makedirs(os.path.join(output_path, 'metrics', sites[0]))

    # Calculate for test model
    test_var_season = np.empty([len(variables), len(seasons)]) * np.nan
    
    # Construct file pattern based on naming convention
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path, f'*{test_model}*mo*{sites[0]}.nc'))
    else:
        test_model_clean = ''.join(e for e in test_model if e.isalnum()).lower()
        test_file = glob.glob(os.path.join(test_path, f"{sites[0][:3]}{test_model_clean}mon{sites[0][3:5].upper()}*.nc"))
    
    print(f'test_file: {test_file}')
    
    try:
        if len(test_file) > 0:
            # Open dataset with xarray
            test_ds = xr.open_dataset(test_file[0])
            print(f'test_model: {test_model}')
            
            # Process each variable
            for j, variable in enumerate(variables): 
                try:
                    if variable in test_ds:
                        # Extract the variable and calculate annual cycle
                        da = test_ds[variable]
                        test_var_season[j, :] = calculate_annual_cycle(da)
                        print(f'after: {test_var_season[j, :]}')
                    else:
                        print(f"{variable} not found in test dataset")
                except Exception as e:
                    print(f"{variable} could not be processed for {test_model}: {e}")
            
            # Close the dataset
            test_ds.close()
            test_index = 1
        else:
            print('No test file found.')
    except Exception as e:
        print(f'No monthly ACI data for test model were found: {e}')

    # Calculate for observational data (specified by the ACI data structure)
    obs_var_season = np.empty([len(variables), len(seasons), 2]) * np.nan
    print(f'ARM data: {sites[0]}')
    
    # Construct file pattern based on naming convention
    obs_file = glob.glob(os.path.join(obs_path, f"{sites[0][:3]}armdiagsaciclim{sites[0][3:5].upper()}*c1.nc"))
    print(f'obs_file: {obs_file}')
    
    if len(obs_file) == 0:
        print(f"No observational data found for {sites[0]}")
    else:
        # ACI observation files have a special format with mean and std columns
        # We'll use xarray to open it but note the special handling needed
        obs_ds = xr.open_dataset(obs_file[0])
        
        # Process each variable
        for j, variable in enumerate(variables): 
            try:
                if variable in obs_ds:
                    # Extract the variable - for ACI, the format is different with mean and std columns
                    var_data = obs_ds[variable].values
                    
                    # In ACI files, the data is structured differently with mean and std
                    obs_var_season[j, :, 0] = var_data[:, 0]  # mean
                    obs_var_season[j, :, 1] = var_data[:, 1]  # std
                else:
                    print(f"{variable} not found in observation dataset")
            except Exception as e:
                print(f"{variable} not processed for obs: {e}")
        
        # Close the dataset
        obs_ds.close()

    # Calculate CMIP model annual cycle climatology
    cmip_var_season = np.empty([len(ref_models), len(variables), len(seasons)]) * np.nan
 
    for i, ref_model in enumerate(ref_models):
        # Construct file pattern based on naming convention
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path, f"*{ref_model}*acimo*{sites[0]}.nc"))
        else:
            ref_model_name = cmip_ver + ''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path, f"{sites[0]}/{sites[0][:3]}{ref_model_name}acimon{sites[0][3:5].upper()}*.nc"))
        
        print(f'ref_model: {ref_model}')
        
        if not ref_file:
            print(f"{ref_model} not found!")
        else:
            # Open dataset with xarray
            ref_ds = xr.open_dataset(ref_file[0])
            
            # Process each variable
            for j, variable in enumerate(variables): 
                try:
                    if variable in ref_ds:
                        # Extract the variable and calculate annual cycle
                        da = ref_ds[variable]
                        tmp_annual = calculate_annual_cycle(da)
                        
                        # Check for invalid model output (all zeros)
                        if np.count_nonzero(tmp_annual == 0) == 12:
                            tmp_annual[:] = np.nan  # set to missing if model output is invalid
                        
                        cmip_var_season[i, j, :] = tmp_annual
                        print(f"{ref_model}: {cmip_var_season[i, j, :]}")
                    else:
                        print(f"{variable} not found in {ref_model} dataset")
                except Exception as e:
                    print(f"{variable} could not be processed for {ref_model}: {e}")
            
            # Close the dataset
            ref_ds.close()
    
    # Calculate multi-model mean
    mmm_var_season = np.nanmean(cmip_var_season, axis=0)
    cmip_index = 1
    
    # If none of the CMIP is valid, cease the table output
    if len(np.where(np.isfinite(mmm_var_season))[0]) == 0:
        cmip_index = 0
        print('No monthly ACI data for CMIP models were found.')
    
    # Save data in csv format in metrics folder
    for j, variable in enumerate(variables):
        if test_index == 1: 
            try:
                np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_test_annual_cycle_{sites[0]}.csv",
                          test_var_season[j, :])
            except Exception as e:
                print(f'No monthly ACI data for testmodel were stored: {e}')
        
        if cmip_index == 1: 
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_mmm_annual_cycle_{sites[0]}.csv",
                      mmm_var_season[j, :])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_cmip_annual_cycle_{sites[0]}.csv",
                      cmip_var_season[:, j, :])
        
        np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_obs_annual_cycle_{sites[0]}.csv",
                  obs_var_season[j, :, 0])

        # Reference standard deviation
        data = obs_var_season[j, :, 0]
        refstd = data.std(ddof=1)  # Reference standard deviation

        # Compute and save stddev and correlation coefficient of models for taylor diagram
        if test_index == 1:
            try:
                test_sample = np.array([test_var_season[j, :].std(ddof=1), 
                                       np.corrcoef(data, test_var_season[j, :])[0, 1]])
                np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_test_annual_cycle_std_corr_{sites[0]}.csv",
                          test_sample)
            except Exception as e:
                print(f'No monthly ACI data std for testmodel were stored: {e}')
        
        if cmip_index == 1:
            mod_num = len(ref_models)
            m_all = [cmip_var_season[x, j, :] for x in range(mod_num)]
            cmip_samples = np.array([[m.std(ddof=1), np.corrcoef(data, m)[0, 1]] for m in m_all])
            mmm_sample = np.array([mmm_var_season[j, :].std(ddof=1), 
                                  np.corrcoef(data, mmm_var_season[j, :])[0, 1]])
            
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_mmm_annual_cycle_std_corr_{sites[0]}.csv",
                      mmm_sample)
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_cmip_annual_cycle_std_corr_{sites[0]}.csv",
                      cmip_samples)
        
        # Save observation statistics
        obs_sample = np.array([refstd, 1.0])
        np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_obs_annual_cycle_std_corr_{sites[0]}.csv",
                  obs_sample)
        
        
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_aci_line_plot(parameter):
    """Generate line plots of annual cycles"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites
    
    # Control flags for data availability
    test_index = 0
    cmip_index = 0
    
    # Create output figures directory if it doesn't exist
    if not os.path.exists(os.path.join(output_path, 'figures', sites[0])):
        os.makedirs(os.path.join(output_path, 'figures', sites[0])) 

    # Process each variable
    var_longname = [varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        # Try to load test data
        try:
            test_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_test_annual_cycle_{sites[0]}.csv")
            test_index = 1
        except Exception as e:
            print(f'No test model monthly ACI data metrics found: {e}')
            test_index = 0
        
        # Try to load CMIP data
        try:
            mmm_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_mmm_annual_cycle_{sites[0]}.csv")
            cmip_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_cmip_annual_cycle_{sites[0]}.csv")
            mod_num = cmip_data.shape[0]
            cmip_index = 1
        except Exception as e:
            mod_num = 0
            cmip_index = 0
        
        # Load observational data
        try:
            obs_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_obs_annual_cycle_{sites[0]}.csv")
        except Exception as e:
            print(f"Error loading observation data: {e}")
            continue
        
        # Start Plotting
        fig = plt.figure(figsize=(10, 6))  # Create figure with better default size
        ax = fig.add_axes([0.12, 0.12, 0.82, 0.81])  # Create axes
        xax = np.arange(1, 13, 1)  # Monthly x-axis
        
        # Plot CMIP models if available
        if cmip_index == 1:
            for mod_ind in range(mod_num):
                ax.plot(xax, cmip_data[mod_ind, :], 'grey', lw=1)
            ann_mean = np.nanmean(mmm_data[:])
            ax.plot(xax, mmm_data[:], 'b', label=f'MMM: {ann_mean:.2f}', lw=3)
        
        # Plot test model if available
        if test_index == 1:
            ann_mean = np.nanmean(test_data[:])
            ax.plot(xax, test_data[:], 'r', label=f'MOD: {ann_mean:.2f}', lw=3)
        
        # Plot observational data
        ann_mean = np.nanmean(obs_data[:])
        ax.plot(xax, obs_data[:], marker='o', color='black', ms=5, label=f'OBS: {ann_mean:.2f}', lw=3)

        # Configure x-axis
        # Use either month names or provided seasons
        if len(seasons) == 12:
            my_xticks = seasons
        else:
            my_xticks = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
            
        plt.xticks(xax, my_xticks)
        plt.xlim(1, 12)
        
        # Site-specific y-axis limits
        if sites[0] == 'sgpc1' and variable[0:3] == 'ccn': 
            plt.ylim(0, 2000)
        elif sites[0] == 'enac1' and variable[0:3] == 'ccn': 
            plt.ylim(0, 500)
        elif variable == 'cpc':
            if test_index == 1:
                ydn = np.nanmin([obs_data, test_data]) - 100
                yup = np.nanmax([obs_data, test_data]) + 100
            else:
                ydn = np.nanmin(obs_data) - 100
                yup = np.nanmax(obs_data) + 100
            plt.ylim(ydn, yup)
        elif variable == 'cod': 
            plt.ylim(0, 50)
        
        # Add title and labels
        plt.title(f'Annual Cycle: {var_longname[j]} at {sites[0]}', fontsize=15)
        plt.xlabel('Month', fontsize=15)
        plt.ylabel(var_longname[j])
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        plt.legend(loc='best', prop={'size': 12})

        # Save figures
        if variable[0] == 'c':
            figname = f"aerosol_annual_cycle_{variable}_{sites[0]}.png"
        else:
            figname = f"aerosol_annual_cycle_chemical_{variable}_{sites[0]}.png"
            
        fig.savefig(f"{output_path}/figures/{sites[0]}/{figname}")
        plt.close(fig)


#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_aci_taylor_diagram(parameter):
    """Generate Taylor diagrams to compare model performance"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    sites = parameter.sites
    
    # Control flags for data availability
    test_index = 0
    cmip_index = 0
    
    # Create output figures directory if it doesn't exist
    if not os.path.exists(os.path.join(output_path, 'figures', sites[0])):
        os.makedirs(os.path.join(output_path, 'figures', sites[0])) 

    # Process each variable
    var_longname = [varid_longname[x] for x in variables]
    for j, variable in enumerate(variables):
        # Try to load test data statistics
        try:
            test_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_test_annual_cycle_std_corr_{sites[0]}.csv")
            test_index = 1
        except Exception as e:
            print(f'No test model monthly ACI data metrics found: {e}')
            test_index = 0
        
        # Try to load CMIP data statistics
        try:
            mmm_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_mmm_annual_cycle_std_corr_{sites[0]}.csv")
            cmip_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_cmip_annual_cycle_std_corr_{sites[0]}.csv")
            mod_num = cmip_data.shape[0]
            cmip_index = 1
        except Exception as e:
            mod_num = 0
            cmip_index = 0
        
        # Load observational data statistics
        try:
            obs_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_obs_annual_cycle_std_corr_{sites[0]}.csv")
        except Exception as e:
            print(f"Error loading observation data statistics: {e}")
            continue
        
        # Observational annual mean must be valid for Taylor diagram
        if np.isfinite(obs_data[0]):
            try:
                # Create figure for Taylor diagram
                fig = plt.figure(figsize=(8, 8))
                refstd = obs_data[0]
                dia = TaylorDiagram(refstd, fig=fig, rect=111, label="Reference")

                # Add samples to Taylor diagram
                if cmip_index == 1:
                    # Add CMIP models
                    for i, (stddev, corrcoef) in enumerate(cmip_data):
                        dia.add_sample(stddev, corrcoef, marker='.', ms=10, c='grey')
                    # Add multi-model mean
                    dia.add_sample(mmm_data[0], mmm_data[1], marker='.', ms=15, c='b', label='MMM')
                
                # Add test model if available
                if test_index == 1:
                    dia.add_sample(test_data[0], test_data[1], marker='.', ms=15, c='red', label='MOD')

                # Add RMS contours and labels
                contours = dia.add_contours(colors='0.5')
                plt.clabel(contours, inline=1, fontsize=10)
                plt.title(f"{var_longname[j]} - {sites[0]}")

                # Add figure legend based on available data
                if (cmip_index + test_index) == 0:
                    lg_item = [dia.samplePoints[0]]
                elif (cmip_index + test_index) == 1:
                    lg_item = [dia.samplePoints[0], dia.samplePoints[-1]]
                elif (cmip_index + test_index) == 2:
                    lg_item = [dia.samplePoints[0], dia.samplePoints[-2], dia.samplePoints[-1]]
                    
                fig.legend(lg_item,
                          [p.get_label() for p in lg_item],
                          numpoints=1, loc='upper right', prop={'size': 10})

                # Save figure with appropriate name
                if variable[0] == 'c':
                    figname = f"aerosol_annual_cycle_{variable}_taylor_diagram_{sites[0]}.png"
                else:
                    figname = f"aerosol_annual_cycle_chemical_{variable}_taylor_diagram_{sites[0]}.png"
                
                fig.savefig(f"{output_path}/figures/{sites[0]}/{figname}")
                plt.close(fig)
                
            except Exception as e:    
                print(f"Taylor diagram not generated for {variable}: plotting error - {e}")
        else:
            print(f"Taylor diagram not generated for {variable}: observation annual mean not valid")
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
    
    
