#===========================================================================================================================
# Program for generate precipitation PDF from hourly data
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ----------------------------------------------------------------------------------------------------
    # Xiaojian Zheng - Dec 2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### change the input/output format & the local time offset to site-dependent
    # ### minor fix on the legends, add multi-model mean on the plots
    # ### extend the pdf to all the four seasons
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
from copy import deepcopy
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid
from .varid_dict import varid_longname
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

def var_pdf_daily(da, season, years):
    """Calculate daily PDF data for each variable using xarray.
    
    Parameters
    ----------
    da : xarray.DataArray
        DataArray containing the variable data
    season : str
        Season to select ('JJA', 'SON', 'DJF', 'MAM')
    years : list
        List of years to process
        
    Returns
    -------
    np.ndarray
        Flattened array of daily data for the selected season across all years
    """
    # Set season start month
    if season == 'JJA':
        mo0 = 6
    elif season == 'SON': 
        mo0 = 9
    elif season == 'DJF': 
        mo0 = 12
    elif season == 'MAM': 
        mo0 = 3
    
    # Initialize array for storing yearly data
    var_da_year = np.empty([len(years), 90]) * np.nan
    
    # Process each year
    for iy, year in enumerate(years):
        # Set season start and end bounds using calendar-safe string dates
        # (avoid pandas datetime arithmetic, which can create invalid dates for
        # non-Gregorian calendars such as noleap)
        if season == 'JJA':
            start_time = f"{year}-06-01"
            end_time = f"{year}-09-01"
        elif season == 'SON':
            start_time = f"{year}-09-01"
            end_time = f"{year}-12-01"
        elif season == 'DJF':
            start_time = f"{year}-12-01"
            end_time = f"{year+1}-03-01"
        elif season == 'MAM':
            start_time = f"{year}-03-01"
            end_time = f"{year}-06-01"
        
        try:
            # Select data for this season
            var_slice = da.sel(time=slice(start_time, end_time))
            
            # Check if we got data
            if len(var_slice.time) == 0:
                print(f"No data found for {season} {year}")
                continue
            
            # Copy to output array, handling different lengths
            # (use the min of 90 or the length of the selected data)
            data_length = min(90, len(var_slice))
            var_da_year[iy, :data_length] = var_slice.values[:data_length]
            
            # Apply unit conversions if needed - these are now handled by convert_units function
            
        except Exception as e:
            print(f"Error processing {season} {year}: {e}")
    
    # Reshape to a single flat array
    var_da = np.reshape(var_da_year, (90 * len(years)))
    return var_da

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def pdf_daily_data(parameter):
    """Calculate daily PDF data for precipitation and other variables"""
    variables = parameter.variables
    test_path = parameter.test_data_path
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    seasons = parameter.season
    sites = parameter.sites   

    test_model = parameter.test_data_set 
    test_styr = parameter.test_start_year
    test_edyr = parameter.test_end_year
    ref_models = parameter.ref_models
    arm_name = parameter.arm_filename
    cmip_ver = cmip_path.split('/')[-1]

    print('============================================================')
    print(f'Create Precipitation PDF: {sites[0]}')
    print('============================================================')
    
    # Create output directory if it doesn't exist
    if not os.path.exists(os.path.join(output_path, 'metrics', sites[0])):
        os.makedirs(os.path.join(output_path, 'metrics', sites[0]))
    
    # Calculate for test model
    test_findex = 0  # preset of test model indicator
    years_test = list(range(test_styr, test_edyr))  # make years list of test model
    
    test_var_season = np.empty([len(variables), len(years_test)*90, len(seasons)]) * np.nan

    if not arm_name:
        test_file = glob.glob(os.path.join(test_path, f'*{test_model}*_da_*.nc'))  # read in test data
    else:
        test_model_clean = ''.join(e for e in test_model if e.isalnum()).lower()
        print(f'test_model: {test_model_clean}')
        test_file = glob.glob(os.path.join(test_path, f"{sites[0][:3]}{test_model_clean}day{sites[0][3:5].upper()}*.nc"))

    if len(test_file) == 0:
        print(f'No daily data for test model were found: {sites[0]}')
    else:
        # Test model exists
        test_findex = 1 
        
        # Open dataset with xarray
        test_ds = xr.open_dataset(test_file[0])
        print(f'test_model: {test_model}')

        for j, variable in enumerate(variables): 
            for k, season in enumerate(seasons):
                try:
                    if variable in test_ds:
                        # Extract the variable as a DataArray
                        da = test_ds[variable]
                        
                        # Apply unit conversions if needed
                        da = convert_units(da)
                        
                        # Calculate daily PDF data
                        test_var_da = var_pdf_daily(da, season, years_test)
                        test_var_season[j, :, k] = test_var_da
                    else:
                        print(f"{variable} not found in test dataset")
                except Exception as e:
                    print(f"{variable} {season} not processed for {test_model}: {e}")
                    print('!!please check the start and end year in your parameter file')
                    test_findex = 0
        
        # Close the dataset
        test_ds.close()

    # Calculate for observational data
    # Site-dependent time ranges
    site_year_ranges = {
        'sgpc1': (2004, 2015),
        'enac1': (2016, 2019),
        'nsac1': (2001, 2015),
        'twpc1': (1998, 2009),
        'twpc2': (1999, 2010),
        'twpc3': (2003, 2010),
        'maom1': (2014, 2015)
    }
    
    # Get years for current site, with fallback to a default range
    if sites[0] in site_year_ranges:
        years_obs = list(range(*site_year_ranges[sites[0]]))
    else:
        # Default to a reasonable range if site not in dictionary
        years_obs = list(range(2000, 2015))
        print(f"Warning: No predefined year range for site {sites[0]}, using default 2000-2015")
    
    obs_var_season = np.empty([len(variables), len(years_obs)*90, len(seasons)]) * np.nan
    
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path, '*ARMdiag*daily*.nc'))
    else:
        obs_file = glob.glob(os.path.join(obs_path, f"{sites[0][:3]}armdiagsday{sites[0][3:5].upper()}*c1.nc"))
   
    print('ARM data')
    
    if len(obs_file) == 0:
        print(f"No observational data found for {sites[0]}")
    else:
        # Open dataset with xarray
        obs_ds = xr.open_dataset(obs_file[0])
        
        for j, variable in enumerate(variables): 
            for k, season in enumerate(seasons):
                try:
                    if variable in obs_ds:
                        # Extract the variable as a DataArray
                        da = obs_ds[variable]
                        
                        # Apply unit conversions if needed
                        da = convert_units(da)
                        
                        # Calculate daily PDF data
                        obs_var_da = var_pdf_daily(da, season, years_obs)
                        obs_var_season[j, :, k] = obs_var_da
                    else:
                        print(f"{variable} not found in observation dataset")
                except Exception as e:
                    print(f"{variable} {season} not processed for obs: {e}")
        
        # Close the dataset
        obs_ds.close()

    # Calculate cmip model seasonal mean climatology
    years = list(range(1979, 2006))  # make years list of CMIP models
    cmip_var_season = np.empty([len(ref_models), len(variables), len(years)*90, len(seasons)]) * np.nan
 
    for i, ref_model in enumerate(ref_models):
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path, f'*{ref_model}*_da_*.nc'))
        else:
            ref_model_name = cmip_ver + ''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path, f"{sites[0]}/{sites[0][:3]}{ref_model_name}day{sites[0][3:5].upper()}*.nc"))
        
        print(f'ref_model: {ref_model}')
        
        if not ref_file:
            print(f"{ref_model} not found!")
        else:
            # Open dataset with xarray
            ref_ds = xr.open_dataset(ref_file[0])
            
            for j, variable in enumerate(variables): 
                for k, season in enumerate(seasons):
                    try:
                        if variable in ref_ds:
                            # Extract the variable as a DataArray
                            da = ref_ds[variable]
                            
                            # Apply unit conversions if needed
                            da = convert_units(da)
                            
                            # Calculate daily PDF data
                            cmip_var_da = var_pdf_daily(da, season, years)
                            cmip_var_season[i, j, :, k] = cmip_var_da
                        else:
                            print(f"{variable} not found in {ref_model} dataset")
                    except Exception as e:
                        print(f"{variable} {season} not processed for {ref_model}: {e}")
            
            # Close the dataset
            ref_ds.close()
    
    # Calculate multi-model mean
    mmm_var_season = np.nanmean(cmip_var_season, axis=0)
    
    # Save data in csv format in metrics folder
    for j, variable in enumerate(variables):
        for k, season in enumerate(seasons):
            if test_findex == 1:
                np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_test_pdf_daily.csv", 
                          test_var_season[j, :, k])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_mmm_pdf_daily.csv", 
                      mmm_var_season[j, :, k])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_cmip_pdf_daily.csv", 
                      cmip_var_season[:, j, :, k])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_obs_pdf_daily.csv", 
                      obs_var_season[j, :, k])

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def accum(list):
    """Sequential accumulation of the original list"""
    result = []
    for i in range(len(list)):
        result.append(sum(list[:i+1]))
    return result
    
def calculate_pdf(var):
    bins_width=[0.0025*1.2**(x) for x in range(55)]
    bins=accum(bins_width)
    bins=[x for x in bins]
    precip_cutoff=0.03-0.0025/2 
    ind = np.where(var>precip_cutoff)
    var_da=var[ind]
    y,binEdges=np.histogram(var_da,bins=bins,density=True)
    cumulative = np.cumsum(y*(binEdges[1:]-binEdges[:-1]))
    wday_ob=100.0*np.size(var_da)/np.size(var)
    return y, binEdges  

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def pdf_daily_plot(parameter):
    """Plot PDFs using daily mean data"""
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    ref_models = parameter.ref_models
    sites = parameter.sites 

    var_longname = [varid_longname[x] for x in variables]
    mod_num = len(ref_models)
    
    # Create output figures directory if it doesn't exist
    if not os.path.exists(os.path.join(output_path, 'figures', sites[0])):
        os.makedirs(os.path.join(output_path, 'figures', sites[0]))
    
    # Process each variable and season
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            try:
                # Try to load test data
                test_path = f"{output_path}/metrics/{sites[0]}/{variable}_{season}_test_pdf_daily.csv"
                test_data = genfromtxt(test_path)
                test_findex = 1
            except Exception as e:
                print(f"Could not load test data for {variable}_{season}: {e}")
                test_findex = 0
            
            try:
                # Load MMM, observation, and CMIP data
                mmm_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_mmm_pdf_daily.csv")
                obs_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_obs_pdf_daily.csv")
                cmip_data = genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_cmip_pdf_daily.csv")
                mod_num = cmip_data.shape[0]
                
                ######################Use same method to calculate PDFs for obs, model and cmip multi-models.
                # Create figures for two different PDF representations
                fig = plt.figure(figsize=(8, 6))  # Create frequency plot figure
                ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])  # Create axes
                
                fig1 = plt.figure(figsize=(8, 6))  # Create amount plot figure
                ax1 = fig1.add_axes([0.15, 0.15, 0.8, 0.8])  # Create axes
                
                # Plot test model if available
                if test_findex == 1:
                    y, binEdges = calculate_pdf(test_data)
                    y0 = deepcopy(y)
                    y[y0 == 0] = np.nan  # Replace zeros with NaN for plotting
                    ax.plot(0.5*(binEdges[1:]+binEdges[:-1]), y, 'r', lw=3, label='MOD')
                    
                    # Calculate and plot precipitation amount
                    y1 = y*0.5*(binEdges[1:]+binEdges[:-1])
                    y10 = deepcopy(y1)
                    y1[y10 == 0] = np.nan
                    ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]), y1, 'r', lw=3, label='MOD')
                
                # Plot observation data
                y, binEdges = calculate_pdf(obs_data)
                y0 = deepcopy(y)
                y[y0 == 0] = np.nan
                ax.plot(0.5*(binEdges[1:]+binEdges[:-1]), y, 'k', lw=3, label='OBS')
                
                # Calculate and plot precipitation amount
                y1 = y*0.5*(binEdges[1:]+binEdges[:-1])
                y10 = deepcopy(y1)
                y1[y10 == 0] = np.nan
                ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]), y1, 'k', lw=3, label='OBS')
                
                # Storage for multi-model mean calculation
                ym_all = np.empty([0])*np.nan
                
                # Plot individual CMIP models
                for imod in range(mod_num):
                    y, binEdges = calculate_pdf(cmip_data[imod, :])
                    y0 = deepcopy(y)
                    y[y0 == 0] = np.nan
                    ax.plot(0.5*(binEdges[1:]+binEdges[:-1]), y, 'grey', lw=1)
                    
                    # Calculate and plot precipitation amount
                    y1 = y*0.5*(binEdges[1:]+binEdges[:-1])
                    y10 = deepcopy(y1)
                    y1[y10 == 0] = np.nan
                    ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]), y1, 'grey', lw=1)
                    
                    # Accumulate for multi-model mean
                    ym_all = np.concatenate((ym_all, y))
                
                # Calculate and plot multi-model mean
                ym_all1 = np.reshape(ym_all, (mod_num, len(y)))
                ymmm = np.nanmean(ym_all1, axis=0)
                ymmm0 = deepcopy(ymmm)
                ymmm[ymmm0 == 0] = np.nan
                ax.plot(0.5*(binEdges[1:]+binEdges[:-1]), ymmm, 'b', lw=3, label='MMM')
                
                # Calculate and plot multi-model mean precipitation amount
                ymmm1 = ymmm*0.5*(binEdges[1:]+binEdges[:-1])
                ymmm10 = deepcopy(ymmm1)
                ymmm1[ymmm10 == 0] = np.nan
                ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]), ymmm1, 'b', lw=3, label='MMM')
                
                # Add legends
                ax.legend(loc='best', prop={'size': 10})
                ax1.legend(loc='best', prop={'size': 10})
                
                # Configure axes for frequency plot
                ax.set_xscale('log')
                ax.set_yscale('log')
                ax.set_xlim([0.05, 200])
                ax.set_ylim([0.0001, 20])
                ax.set_ylabel('Frequency')
                ax.set_xlabel('Precipitation rate (mm/day)')
                ax.set_title(f"{var_longname[j]} PDF - {season} - {sites[0]}")
                
                # Configure axes for amount plot
                ax1.set_xlim([0.05, 200])
                ax1.set_ylim([0.01, 1])
                ax1.set_xscale('log')
                ax1.set_yscale('log')
                ax1.set_ylabel('Precipitation Amount (mm/day)')
                ax1.set_xlabel('Precipitation rate (mm/day)')
                ax1.set_title(f"{var_longname[j]} Amount PDF - {season} - {sites[0]}")
                
                # Save figures
                fig.savefig(f"{output_path}/figures/{sites[0]}/{variable}_{season}_pdf1_daily_{sites[0]}.png")
                fig1.savefig(f"{output_path}/figures/{sites[0]}/{variable}_{season}_pdf2_daily_{sites[0]}.png")
                
                # Close figures to free memory
                plt.close(fig)
                plt.close(fig1)
                
            except Exception as e:
                print(f"Error processing {variable} {season}: {e}")

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
