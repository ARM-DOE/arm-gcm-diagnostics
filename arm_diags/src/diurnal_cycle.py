#===========================================================================================================================
# Program for generate precipitation diurnal cycle from hourly data -- Originally written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V4 Development
    # ----------------------------------------------------------------------------------------------------
    # Refactored to use xarray instead of cdms2/cdutil
    # Maintained original functionality while modernizing the code
    # ----------------------------------------------------------------------------------------------------

#===========================================================================================================================
import os
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid
from .varid_dict import varid_longname
from scipy.optimize import curve_fit
import pandas as pd
from datetime import datetime

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

def var_diurnal_cycle(ds, var_name, season, tres, styr, edyr):
    """Calculate diurnal cycle climatology of each variable using xarray."""
    # Check if variable exists in dataset
    if var_name not in ds:
        print(f"Variable {var_name} not found in dataset")
        return np.full(24 if tres == '1hr' else 8, np.nan)
    
    # Extract the variable
    da = ds[var_name]
    
    # Set time resolution specific variables
    tres_id = 24 if tres == '1hr' else 8
    
    # Create array for storing yearly data
    years = list(range(styr, edyr))
    var_dc_year = np.empty([len(years), tres_id]) * np.nan
    
    # Select data for each year and season
    for iy, year in enumerate(years):
        try:
            # Set start and end times for season selection
            if season == 'ANN':
                start_time = f"{year}-01-01"
                end_time = f"{year+1}-01-01" if year < edyr-1 else f"{year}-12-31"
                days_in_season = 365
            elif season == 'JJA':
                start_time = f"{year}-06-01"
                end_time = f"{year}-09-01"
                days_in_season = 92
            elif season == 'SON':
                start_time = f"{year}-09-01"
                end_time = f"{year}-12-01"
                days_in_season = 91
            elif season == 'DJF':
                # Handle winter (crosses year boundary)
                start_time = f"{year}-12-01"
                end_time = f"{year+1}-03-01" if year < edyr-1 else f"{year+1}-02-28"
                days_in_season = 90
            elif season == 'MAM':
                start_time = f"{year}-03-01"
                end_time = f"{year}-06-01"
                days_in_season = 92
            
            # Select data for this season
            var_yr = da.sel(time=slice(start_time, end_time))
            
            # Just warn about fraction of missing data
            if len(var_yr.time) < days_in_season * tres_id * 0.8:  # Allow for some missing data
                missing_percentage = 100 * (1 - len(var_yr.time) / (days_in_season * tres_id))
                print(f"Warning: {year} {season} has {missing_percentage:.1f}% missing data - using available data anyway")
                
            # Group by hour of day and calculate mean
            # First ensure time is properly decoded as datetime
            if not np.issubdtype(var_yr.time.dtype, np.datetime64):
                # If time is not a datetime, extract hour manually based on data frequency
                # Calculate hours based on data frequency and position in day
                if tres == '1hr':
                    # For 1-hourly data, use modulo 24 for hour of day
                    hours = np.arange(len(var_yr.time)) % 24
                elif tres == '3hr':
                    # For 3-hourly data, use modulo 8 * 3 for hour of day
                    hours = (np.arange(len(var_yr.time)) % 8) * 3
                else:
                    print(f"Error: Unknown time resolution {tres}")
                    var_dc_year[iy, :] = np.nan
                    continue
                
                # Create a new coordinate for hour
                var_yr = var_yr.assign_coords(hour=('time', hours))
                var_hr = var_yr.groupby('hour').mean(dim='time')
            else:
                # Regular approach if time is properly decoded
                try:
                    var_hr = var_yr.groupby('time.hour').mean(dim='time')
                except AttributeError:
                    # Fallback if hour attribute is missing
                    # Extract hour from time using xarray's dt accessor
                    hours = var_yr.time.dt.hour.values
                    var_yr = var_yr.assign_coords(hour=('time', hours))
                    var_hr = var_yr.groupby('hour').mean(dim='time')
            
            # Convert to numpy and store
            var_dc_year[iy, :] = var_hr.values
            
            # Apply unit conversions
            if var_name == 'tas':
                var_dc_year[iy, :] = var_dc_year[iy, :] - 273.15
            
            if var_name == 'pr':
                var_dc_year[iy, :] = var_dc_year[iy, :] * 3600.0 * 24.0
                
        except Exception as e:
            print(f"Error processing {year} {season}: {e}")
            var_dc_year[iy, :] = np.nan
    
    # Take mean across years
    var_dc = np.nanmean(var_dc_year, axis=0)
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
    print(f'Create Precipitation Diurnal Cycles: {sites[0]}')
    print('============================================================')

    # Calculate for test model
    test_findex = 0  # preset of test model indicator
    
    if not arm_name:
        test_file = glob.glob(os.path.join(test_path, f"*{test_model}*hr*.nc"))  # read in hourly test data
    else:
        test_model = ''.join(e for e in test_model if e.isalnum()).lower()
        print(test_path, test_model, f"{sites[0][:3]}{test_model}*hr{sites[0][3:5].upper()}")
        test_file = glob.glob(os.path.join(test_path, f"{sites[0][:3]}{test_model}*hr{sites[0][3:5].upper()}*.nc"))

    if len(test_file) == 0:
        print(f'No diurnal data for test model were found: {sites[0]}')
    else:
        # Test model exists
        test_findex = 1
        
        # Initialize the indicator for temporal res of testmodel
        test_tres = test_file[0].split(test_model)[-1][:3]  # e.g., '3hr', '1hr'
        
        # Open dataset with xarray
        test_ds = xr.open_dataset(test_file[0])
        test_tidlen = 24 if test_tres == '1hr' else 8
        
        test_var_season = np.empty([len(variables), test_tidlen, len(seasons)]) * np.nan
        
        print(f'Processing diurnal data for test_model {test_model} with Tres of {test_tres}')
        
        for j, variable in enumerate(variables):
            for k, season in enumerate(seasons):
                try:
                    test_var_dc = var_diurnal_cycle(test_ds, variable, season, test_tres, test_styr, test_edyr)
                    test_var_season[j, :, k] = test_var_dc
                except Exception as e:
                    print(f"{variable} {season} not processed for {test_model}: {e}")
                    print('!!please check the start and end year in your parameter file')
                    test_findex = 0
        
        # Close the dataset
        test_ds.close()

    # Calculate for observational data
    obs_var_season = np.empty([len(variables), 24, len(seasons)]) * np.nan
    
    if not arm_name:
        obs_file = glob.glob(os.path.join(obs_path, '*ARMdiag_domain_diurnal*.nc'))  # read in diurnal test data
    else:
        obs_file = glob.glob(os.path.join(obs_path, f"{sites[0][:3]}armdiagsmondiurnal{sites[0][3:5].upper()}.c1.nc"))
    
    print('ARM data')
    
    if len(obs_file) == 0:
        print(f"No observational data found for {sites[0]}")
    else:
        # Open dataset with xarray
        obs_ds = xr.open_dataset(obs_file[0])
        
        for j, variable in enumerate(variables):
            try:
                if variable in obs_ds:
                    # Extract variable
                    var = obs_ds[variable].values
                    
                    # Reshape to (years, months, hours)
                    var_dc = np.reshape(var, (int(var.shape[0] / 12 / 24), 12, 24))
                    var_dc = np.nanmean(var_dc, axis=0)  # Average over years
                    
                    # Extend the var for all seasons
                    var_dc12 = np.concatenate((var_dc, var_dc), axis=0)
                    
                    for k, season in enumerate(seasons):
                        if season == 'ANN':
                            obs_var_dc = np.nanmean(var_dc12[0:12, :], axis=0)
                        elif season == 'MAM':
                            obs_var_dc = np.nanmean(var_dc12[2:5, :], axis=0)
                        elif season == 'JJA':
                            obs_var_dc = np.nanmean(var_dc12[5:8, :], axis=0)
                        elif season == 'SON':
                            obs_var_dc = np.nanmean(var_dc12[8:11, :], axis=0)
                        elif season == 'DJF':
                            obs_var_dc = np.nanmean(var_dc12[11:14, :], axis=0)
                        
                        # Convert var units
                        if variable == 'tas':
                            obs_var_dc = obs_var_dc - 273.15
                        if variable == 'pr':
                            obs_var_dc = obs_var_dc * 3600.0 * 24.0
                            
                        # Store processed array
                        obs_var_season[j, :, k] = obs_var_dc
            except Exception as e:
                print(f"{variable} not processed for obs: {e}")
        
        # Close the dataset
        obs_ds.close()

    # Calculate cmip model seasonal mean climatology (diurnal cycles)
    cmip_var_season = np.empty([len(ref_models), len(variables), 8, len(seasons)]) * np.nan
    
    for i, ref_model in enumerate(ref_models):
        if not arm_name:
            ref_file = glob.glob(os.path.join(cmip_path, f"{sites[0]}/*{ref_model}*3hr*.nc"))  # read in cmip data
        else:
            ref_model_name = cmip_ver + ''.join(e for e in ref_model if e.isalnum()).lower()
            ref_file = glob.glob(os.path.join(cmip_path, f"{sites[0]}/{sites[0][:3]}{ref_model_name}3hr{sites[0][3:5].upper()}*.nc"))
        print(os.path.join(cmip_path, f"{sites[0]}/*{ref_model}*3hr*.nc"))
        
        print(f'ref_model: {ref_model}')
        
        if not ref_file:
            print(f"{ref_model} not found!")
        else:
            # Open dataset with xarray
            ref_ds = xr.open_dataset(ref_file[0])
            
            for j, variable in enumerate(variables):
                for k, season in enumerate(seasons):
                    try:
                        cmip_var_season[i, j, :, k] = var_diurnal_cycle(ref_ds, variable, season, '3hr', 1979, 2006)
                    except Exception as e:
                        print(f"{variable} {season} not processed for {ref_model}: {e}")
            
            # Close the dataset
            ref_ds.close()

    # Calculate multi-model mean
    mmm_var_season = np.nanmean(cmip_var_season, axis=0)

    # Save data in csv format in metrics folder
    # Generate new folder given site names
    if not os.path.exists(os.path.join(output_path, 'metrics', sites[0])):
        os.makedirs(os.path.join(output_path, 'metrics', sites[0]))
        
    for j, variable in enumerate(variables):
        for k, season in enumerate(seasons):
            if test_findex == 1:
                np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_test_diurnal_cycle_{test_tres}_{sites[0]}.csv", 
                          test_var_season[j, :, k])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_mmm_diurnal_cycle_{sites[0]}.csv", 
                      mmm_var_season[j, :, k])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_cmip_diurnal_cycle_{sites[0]}.csv", 
                      cmip_var_season[:, j, :, k])
            np.savetxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_obs_diurnal_cycle_{sites[0]}.csv", 
                      obs_var_season[j, :, k])

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def func24(x, p1, p2):
    """Sinusoidal function for fitting diurnal cycles."""
    return p1 * np.sin(2 * np.pi / 24 * x + p2)


def diurnal_cycle_plot(parameter):
    """Plot diurnal cycle climatology."""
    sites = parameter.sites
    variables = parameter.variables
    seasons = parameter.season
    output_path = parameter.output_path
    ref_models = parameter.ref_models

    var_longname = [varid_longname[x] for x in variables]
    mod_num = len(ref_models)

    # Generate new folder given site names
    if not os.path.exists(os.path.join(output_path, 'figures', sites[0])):
        os.makedirs(os.path.join(output_path, 'figures', sites[0]))

    # start the plotting procedure
    for j, variable in enumerate(variables):
        for i, season in enumerate(seasons):
            # check the test model data
            test_findex = 0  # preset of test model indicator
            test_file = glob.glob(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_test_diurnal_cycle_*{sites[0]}.csv")
            
            if len(test_file) == 0:
                print(f'No test model plotted for diurnal cycle: {sites[0]}')
            else:
                test_findex = 1  # test model exists
                test_tres = test_file[0].split('_test_diurnal_cycle_')[-1][:3]  # e.g., '3hr', '1hr'

            # read data
            if test_findex == 1:
                test_data = np.genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_test_diurnal_cycle_{test_tres}_{sites[0]}.csv")
            mmm_data = np.genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_mmm_diurnal_cycle_{sites[0]}.csv")
            obs_data = np.genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_obs_diurnal_cycle_{sites[0]}.csv")
            cmip_data = np.genfromtxt(f"{output_path}/metrics/{sites[0]}/{variable}_{season}_cmip_diurnal_cycle_{sites[0]}.csv")
            mod_num = cmip_data.shape[0]

            # plotting
            fig = plt.figure()  # Create figure
            ax = fig.add_axes([0.10, 0.10, 0.85, 0.85])  # Create axes
            
            # create site-dependent time offset for the local time & plotting range
            if sites[0] == 'sgpc1': local_offset = -6.5; yup = 10
            if sites[0] == 'enac1': local_offset = -2; yup = 6
            if sites[0] == 'nsac1': local_offset = -10; yup = 4
            # for positive offset-24h: make sure the plotting continuity
            if sites[0] == 'twpc1': local_offset = 10-24; yup = 30
            if sites[0] == 'twpc2': local_offset = 11-24; yup = 15
            if sites[0] == 'twpc3': local_offset = 9-24; yup = 30
            if sites[0] == 'maom1': local_offset = -4; yup = 30
            
            xax_3hr = np.array([3.0 * x + local_offset for x in range(8)])
            xax_1hr = np.array([1.0 * x + local_offset for x in range(24)])
            
            # plotting ref models
            mod_phase = np.empty([mod_num])
            mod_amp = np.empty([mod_num])
            
            for mod_ind in range(mod_num):
                # Use curve_fit to extract first harmonic
                popt, pcov = curve_fit(func24, xax_3hr, cmip_data[mod_ind,:], p0=(1.0,0.2))
                p1_mod = popt[0]
                p2_mod = popt[1]
                data_mean = np.mean(cmip_data[mod_ind,:])
                
                # Generate smooth fit line
                ymod_fit = func24(xax_1hr, p1_mod, p2_mod) + data_mean
                
                # Plot the fit
                mod_fit, = ax.plot(np.concatenate((xax_1hr, [x+24 for x in xax_1hr])), 
                                 np.concatenate((ymod_fit, ymod_fit)), 'grey', lw=1)
                
                # Store amp and phase for the harmonic dial
                mod_amp[mod_ind] = p1_mod
                if p1_mod <= 0:
                   p2_mod = 1.5*np.pi - p2_mod
                if p1_mod > 0:
                   p2_mod = 0.5*np.pi - p2_mod
                mod_phase[mod_ind] = p2_mod

            # plotting multi-model mean
            ann_mean = np.nanmean(mmm_data[:])
            
            # Use curve_fit to extract first harmonic for MMM
            popt, pcov = curve_fit(func24, xax_3hr, mmm_data, p0=(1.0,0.2))
            p1_mod = popt[0]
            p2_mod = popt[1]
            data_mean = np.mean(mmm_data)
            
            # Generate smooth fit line
            ymod_fit = func24(xax_1hr, p1_mod, p2_mod) + data_mean
            
            # Plot the data points
            ax.plot(np.concatenate((xax_3hr, [x+24 for x in xax_3hr])), 
                  np.concatenate((mmm_data, mmm_data)), '.b', 
                  label=f'MMM: {ann_mean:.2f}', lw=2, markersize=10)
            
            # Plot the curve fit
            mod_fit, = ax.plot(np.concatenate((xax_1hr, [x+24 for x in xax_1hr])), 
                             np.concatenate((ymod_fit, ymod_fit)), 'b', 
                             label='MMM fit', lw=2)
            
            # Store amplitude and phase for harmonic dial
            mmm_amp = p1_mod
            if p1_mod <= 0:
               p2_mod = 1.5*np.pi - p2_mod
            if p1_mod > 0:
               p2_mod = 0.5*np.pi - p2_mod
            mmm_phase = p2_mod

            # plotting test model
            if test_findex == 1:
                if test_tres == '1hr':
                    test_pxaxis = xax_1hr.copy()
                    n_hours = 24
                else: # 3hr
                    test_pxaxis = xax_3hr.copy()
                    n_hours = 8
                
                ann_mean = np.nanmean(test_data[:])
                
                # Use curve_fit to extract first harmonic for test model
                test_xax = test_pxaxis
                popt, pcov = curve_fit(func24, test_xax, test_data, p0=(1.0,0.2))
                p1_mod = popt[0]
                p2_mod = popt[1]
                data_mean = np.mean(test_data)
                
                # Generate smooth fit line
                ymod_fit = func24(xax_1hr, p1_mod, p2_mod) + data_mean
                
                # Plot data points
                ax.plot(np.concatenate((test_pxaxis, [x+24 for x in test_pxaxis])), 
                      np.concatenate((test_data, test_data)), '.r', 
                      label=f'MOD: {ann_mean:.2f}', lw=2, markersize=10)
                
                # Plot curve fit
                mod_fit, = ax.plot(np.concatenate((xax_1hr, [x+24 for x in xax_1hr])), 
                                 np.concatenate((ymod_fit, ymod_fit)), 'r', 
                                 label='MOD fit', lw=2)
                
                # Store amplitude and phase for harmonic dial
                test_amp = p1_mod
                if p1_mod <= 0:
                   p2_mod = 1.5*np.pi - p2_mod
                if p1_mod > 0:
                   p2_mod = 0.5*np.pi - p2_mod
                test_phase = p2_mod

            # plotting observation
            ann_mean = np.nanmean(obs_data[:])
            
            # Use curve_fit to extract first harmonic for observations
            popt, pcov = curve_fit(func24, xax_1hr, obs_data, p0=(1.0,0.2))
            p1_obs = popt[0]
            p2_obs = popt[1]
            data_mean = np.mean(obs_data)
            
            # Generate smooth fit line
            yobs2 = func24(xax_1hr, p1_obs, p2_obs) + data_mean
            
            # Plot data points
            obs2, = plt.plot(np.concatenate((xax_1hr, [x+24 for x in xax_1hr])), 
                           np.concatenate((obs_data, obs_data)), 'k.', 
                           label=f'OBS: {ann_mean:.2f}', lw=2, markersize=10)
            
            # Plot curve fit
            obs_fit2, = plt.plot(np.concatenate((xax_1hr, [x+24 for x in xax_1hr])), 
                               np.concatenate((yobs2, yobs2)), 'k', 
                               label='OBS fit', lw=2)
            
            # Store amplitude and phase for harmonic dial
            obs2_amp = abs(p1_obs)
            if p1_obs <= 0:
               p2_obs = 1.5*np.pi - p2_obs
            if p1_obs > 0:
               p2_obs = 0.5*np.pi - p2_obs
            obs2_phase = p2_obs

            # Configure plot
            my_xticks = ['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h']
            my_xticks_loc = np.array([3 * x for x in range(8)])
            plt.xticks(my_xticks_loc, my_xticks)
            ax.set_xlim([0, 24])
            ax.legend(scatterpoints=1, loc='best', prop={'size': 10}, framealpha=0.0)
            plt.xlabel('local solar time [hr]')
            plt.ylabel(var_longname[j])
            
            # Save figure
            fig.savefig(f"{output_path}/figures/{sites[0]}/{variable}_{season}_diurnal_cycle_{sites[0]}.png")
            plt.close('all')
           
            # Generate harmonic dial plot: mapping phase and amplitude to Dial
            hup = 3
            if sites[0] == 'twpc1' or sites[0] == 'maom1':
                hup = 10
            if sites[0] == 'enac1':
                hup = 1

            fig2 = plt.figure()
            ax2 = fig2.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    
            size = 50
            ax2.scatter(obs2_phase, obs2_amp, color='k', label='OBS', s=size*2)
            ax2.scatter(mod_phase[:], abs(mod_amp[:]), color='grey', s=size)
            ax2.scatter(mmm_phase, abs(mmm_amp), color='blue', label='MMM', s=size*2)
            
            if test_findex == 1:
                ax2.scatter(test_phase, abs(test_amp), color='r', label='MOD', s=size*2)
                
            ax2.legend(scatterpoints=1, loc='center right', bbox_to_anchor=(1.2, 0.90), prop={'size': 10})
            ax2.set_rmax(hup)
            ax2.set_theta_direction(-1)
            ax2.set_theta_offset(np.pi/2)
            ax2.set_xticklabels(['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h'])
            grid(True)
    
            # Save harmonic diagram
            fig2.savefig(f"{output_path}/figures/{sites[0]}/{variable}_{season}_diurnal_cycle_harmonic_diagram_{sites[0]}.png")
            plt.close('all')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
