#===========================================================================================================================
# Program for generate annual/seasonal table from monthly data
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### change the input/output format to site-dependent
    # ---------------------------------------------------------------------------------------
# V4 Development
    # ---------------------------------------------------------------------------------------
    # Refactored to use xarray instead of cdms2/cdutil
    # Maintained original functionality while modernizing the code
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================

import os
import glob
import numpy as np
import csv
import xarray as xr
from .varid_dict import varid_longname

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

def calculate_seasonal_mean(da, seasons):
    """
    Calculate seasonal climatology of each variable using xarray.
    
    Parameters
    ----------
    da : xarray.DataArray
        DataArray containing the variable data
    seasons : list
        List of seasons to process (e.g., ['ANN', 'DJF', 'MAM', 'JJA', 'SON'])
        
    Returns
    -------
    np.ndarray
        Array of seasonal mean values with dimensions [len(seasons)]
    """
    # Apply unit conversions
    da = convert_units(da)
    
    # Ensure time is available
    if 'time' not in da.dims:
        print(f"Warning: Variable {da.name} has no time dimension")
        return np.full(len(seasons), np.nan)
    
    # Make sure we have a proper time index
    if not np.issubdtype(da.time.dtype, np.datetime64):
        # Try to decode time if possible without printing warning
        try:
            da = xr.decode_cf(da.to_dataset()).get(da.name)
        except Exception as e:
            print(f"Error decoding time: {e}")
            return np.full(len(seasons), np.nan)
    
    # Create an array to store results
    var_season_data = np.empty(len(seasons)) * np.nan
    
    # Calculate seasonal means
    for k, season in enumerate(seasons):
        try:
            if season == 'ANN':
                # Annual mean - all months
                var_season_data[k] = float(da.mean(dim='time').values)
            else:
                # Specific season
                season_da = da.groupby('time.season').mean(dim='time')
                # Map season names to standard format
                season_map = {'DJF': 'DJF', 'MAM': 'MAM', 'JJA': 'JJA', 'SON': 'SON'}
                if season in season_map:
                    if season_map[season] in season_da.season.values:
                        var_season_data[k] = float(season_da.sel(season=season_map[season]).values)
                    else:
                        print(f"Season {season} not found in data")
                else:
                    print(f"Unsupported season: {season}")
        except Exception as e:
            print(f"Error calculating {season} mean: {e}")
    
    return var_season_data

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def seasonal_mean_table(parameter):
    """Calculate seasonal mean climatology using xarray"""
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
    print(f'Create Seasonal Mean Tables: {sites[0]}')
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

    if len(test_file) == 0:
        raise RuntimeError('No monthly data for test model were found.')

    # Open dataset with xarray
    test_ds = xr.open_dataset(test_file[0])
    print(f'test_model: {test_model}')

    # Process each variable
    for j, variable in enumerate(variables): 
        try:
            if variable in test_ds:
                # Extract the variable and calculate seasonal means
                da = test_ds[variable]
                test_var_season[j, :] = calculate_seasonal_mean(da, seasons)
            else:
                print(f"{variable} not found in test dataset")
        except Exception as e:
            print(f"{variable} not processed for {test_model}: {e}")
    
    # Close the dataset
    test_ds.close()

    # Calculate for observational data
    obs_var_season = np.empty([len(variables), len(seasons)]) * np.nan
    print(f'ARM data: {sites[0]}')
    
    # Construct file pattern based on naming convention
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path, f'ARMdiag*monthly_climo*{sites[0]}.nc'))
    else:
        obs_file = glob.glob(os.path.join(obs_path, f"{sites[0][:3]}armdiagsmon{sites[0][3:5].upper()}*c1.nc"))
    
    print(f'obs_file: {obs_file}')
    
    if len(obs_file) == 0:
        print(f"No observational data found for {sites[0]}")
    else:
        # Open dataset with xarray
        obs_ds = xr.open_dataset(obs_file[0])
        
        # Process each variable
        for j, variable in enumerate(variables): 
            try:
                if variable in obs_ds:
                    # Extract the variable and calculate seasonal means
                    da = obs_ds[variable]
                    obs_var_season[j, :] = calculate_seasonal_mean(da, seasons)
                else:
                    print(f"{variable} not found in observation dataset")
            except Exception as e:
                print(f"{variable} not processed for obs: {e}")
        
        # Close the dataset
        obs_ds.close()

    # Calculate CMIP model seasonal mean climatology
    cmip_var_season = np.empty([len(ref_models), len(variables), len(seasons)]) * np.nan
 
    for i, ref_model in enumerate(ref_models):
        # Construct file pattern based on naming convention
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path, f"{sites[0]}/*{ref_model}*mo*{sites[0]}.nc"))
        else:
            ref_model_name = cmip_ver + ''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path, f"{sites[0]}/{sites[0][:3]}{ref_model_name}mon{sites[0][3:5].upper()}*.nc"))
        
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
                        # Extract the variable and calculate seasonal means
                        da = ref_ds[variable]
                        cmip_var_season[i, j, :] = calculate_seasonal_mean(da, seasons)
                    else:
                        print(f"{variable} not found in {ref_model} dataset")
                except Exception as e:
                    print(f"{variable} not processed for {ref_model}: {e}")
            
            # Close the dataset
            ref_ds.close()
    
    # Calculate multi-model mean
    mmm_var_season = np.nanmean(cmip_var_season, axis=0)
    
    # Save data as a table
    header = ['Variables', 'Model', 'Obs', 'Model-Obs', cmip_path.split('/')[-1].upper()]
    var_longname = [varid_longname[x] for x in variables]
    table_data = np.empty([len(variables), len(seasons), 4])

    # Generate tables for each season
    for k, season in enumerate(seasons):
        for j, variable in enumerate(variables):
            table_data[j, k, :] = (
                round(test_var_season[j, k], 3), 
                round(obs_var_season[j, k], 3),
                round(test_var_season[j, k] - obs_var_season[j, k], 3),
                round(mmm_var_season[j, k], 3)
            )
        
        # Write the table to a CSV file
        table_file = f"{output_path}/metrics/{sites[0]}/seasonal_mean_table_{season}_{sites[0]}.csv"
        with open(table_file, 'w') as f1:
            writer = csv.writer(f1, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_NONE)
            writer.writerow(header)
            # Use tuple to generate csv 
            writer.writerows([c] + row.tolist() for c, row in zip(var_longname, table_data[:, k, :]))

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    
    
    
    
