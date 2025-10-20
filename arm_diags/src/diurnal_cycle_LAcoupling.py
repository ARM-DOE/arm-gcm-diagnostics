#===========================================================================================================================
# Program for generate the diurnal cycle on Land-Atmosphere Coupling
#---------------------------------------------------------------------------------------------------------------------------
# V4 Development
    # ----------------------------------------------------------------------------------------------------
    # Cheng Tao - Jul2024 @ LLNL
    # ### Diurnal cycle of SH, LH, T_srf, RH_srf, LCL, PBL
    # ----------------------------------------------------------------------------------------------------
    # Refactored to use xarray instead of cdms2/cdutil
    # Maintained original functionality while modernizing the code
    # ----------------------------------------------------------------------------------------------------
#===========================================================================================================================
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from .varid_dict import varid_longname
from .taylor_diagram import TaylorDiagram
from .utils import climo
import matplotlib.gridspec as gridspec
import scipy.stats
from scipy import interpolate
import calendar
import math
import xarray as xr

def get_diurnal_cycle_seasons_xr(var, seasons, years, nhour=None):
    """
    Get seasonal data for diurnal cycle analysis using xarray.
    
    Parameters
    ----------
    var : numpy.ndarray
        Input data array of values
    seasons : list
        List of season names
    years : list
        List of years to process
    nhour : int, optional
        Number of hours per day in the data. If None, will be determined from data.
    
    Returns
    -------
    numpy.ndarray
        Array with shape [nyears, nseasons, 365, nhour] containing the diurnal cycle data
    """
    nyears = len(years)
    nseasons = len(seasons)
    t0 = 0
    
    # Determine time resolution from the first day's data
    # Assuming data is organized with either 24 hours (hourly) or 8 hours (3-hourly) per day
    time_length = len(var)
    
    # If nhour is explicitly provided, use it
    if nhour is not None:
        print(f"Using user-specified nhour={nhour}")
    # Otherwise try to determine from data
    elif time_length % 24 == 0:  # If divisible by 24, assume hourly data
        nhour = 24
        print(f"Determined nhour=24 (hourly data)")
    elif time_length % 8 == 0:  # If divisible by 8, assume 3-hourly data
        nhour = 8
        print(f"Determined nhour=8 (3-hourly data)")
    else:
        # Default to 24 if we can't determine
        nhour = 24
        print(f"Warning: Could not determine hour resolution from data length {time_length}. Using nhour=24.")
    
    # Create output array
    var_seasons = np.zeros((nyears, nseasons, 365, nhour)) * np.nan  # diurnal cycle for each day
    
    for iyear in range(nyears):
        if calendar.isleap(int(years[iyear])):
            nday = 366
        else:
            nday = 365
        
        ntime = int(nday * nhour)
        
        # Make sure we have enough data
        if t0 + ntime <= len(var):
            var1 = var[t0:t0+ntime]
            var1_ext = np.concatenate((var1, var1), axis=0)
            t0 = t0 + ntime
            
            for iseason in range(nseasons):
                if seasons[iseason] == 'ANN':
                    length = int(365 * nhour)
                    var_seasons0 = var1[0:length]
                    var_seasons1 = np.reshape(var_seasons0, (365, nhour))
                    var_seasons[iyear, iseason, :, :] = var_seasons1
                else:
                    # Get starting day for each season
                    if seasons[iseason] == 'MAM':  # March 1
                        t1 = 60 if nday == 366 else 59
                    elif seasons[iseason] == 'JJA':  # June 1
                        t1 = 152 if nday == 366 else 151
                    elif seasons[iseason] == 'SON':  # September 1
                        t1 = 244 if nday == 366 else 243
                    elif seasons[iseason] == 'DJF':  # December 1
                        t1 = 335 if nday == 366 else 334
                    else:
                        print(f"Unrecognized season: {seasons[iseason]}")
                        continue
                    
                    # Extract 90 days starting from the season's start date
                    var_seasons0 = var1_ext[int(t1*nhour):int(t1*nhour)+90*nhour]
                    var_seasons1 = np.reshape(var_seasons0, (90, nhour))
                    var_seasons[iyear, iseason, 0:90, :] = var_seasons1
        else:
            print(f"Warning: Not enough data for year {years[iyear]}")
    
    return var_seasons

def diurnal_cycle_LAcoupling_plot(parameter):
    variables = parameter.variables
    test_path = parameter.test_data_path
    test_model = parameter.test_data_set
    obs_path = parameter.obs_path
    cmip_path = parameter.cmip_path
    output_path = parameter.output_path
    sites = parameter.sites
    varnames = parameter.varnames
    units = parameter.units
    seasons = parameter.season
    nseasons = len(seasons)
    nvariables = len(variables)

    print('test_path: ', test_path)

    # Create output directory if it doesn't exist
    if not os.path.exists(os.path.join(output_path, 'figures', sites[0])):
        os.makedirs(os.path.join(output_path, 'figures', sites[0]))

    #==========================================================================
    # Calculate for test model data
    #==========================================================================
    test_file = glob.glob(os.path.join(test_path, f"{sites[0][:3]}testmodel3hrLAcoupling{sites[0][3:5].upper()}*.nc"))
    print('Processing test_file: ', test_file)
    if test_file:
        # Open dataset with xarray, prevent time decoding issues
        test_ds = xr.open_dataset(test_file[0], decode_times=False)
    else:
        print(f"No test files found for {sites[0]}")
        return
    
    #==========================================================================
    # Calculate for observational data
    #==========================================================================
    print('ARM data', sites[0])
    obs_file = glob.glob(os.path.join(obs_path, f"{sites[0][:3]}armdiagsLAcoupling{sites[0][3:5].upper()}*c1.nc"))
    print('Processing obs_file', obs_file)
    if obs_file:
        # Open dataset with xarray, prevent time decoding issues
        obs_ds = xr.open_dataset(obs_file[0], decode_times=False)
    else:
        print(f"No observation files found for {sites[0]}")
        return
   
    for ivar in range(nvariables):
        #============================
        # Seasons: for observations
        #============================
        try:
            # Extract variable from the dataset
            if variables[ivar] in obs_ds:
                var = obs_ds[variables[ivar]].values
            else:
                print(f"Variable {variables[ivar]} not found in observation dataset. Skipping.")
                continue
                
            years_obs = list(range(2004, 2016))
            nyears_obs = len(years_obs)

            # Process the data with our xarray-compatible function - observation data always has 24 hours (hourly)
            nhour_obs = 24
            var_seasons = get_diurnal_cycle_seasons_xr(var, seasons, years_obs, nhour=nhour_obs)
            
            # Verify the shape of the output data matches what we expect
            if var_seasons.shape[3] != nhour_obs:
                print(f"Warning: Expected {nhour_obs} hours in observation data, but got {var_seasons.shape[3]}. Adjusting output shape.")
                # If we got different shape than expected, create a dummy array of correct shape
                var_array = np.empty([nseasons, nhour_obs]) * np.nan
                var_array_err = np.empty([nseasons, nhour_obs]) * np.nan
                continue  # Skip further processing for this variable
            
            narray = nyears_obs * 365
            var_seasons1 = np.empty([nseasons, narray, nhour_obs]) * np.nan
            var_array_err = np.empty([nseasons, nhour_obs]) * np.nan
            var_array = np.empty([nseasons, nhour_obs]) * np.nan
            
            for iseason in range(nseasons):
                for iyear in range(nyears_obs):
                    for iday in range(365):
                        var_seasons1[iseason, 365*iyear+iday, :] = var_seasons[iyear, iseason, iday, :]
     
                array_tmp = var_seasons1[iseason, :, :] 
                data0 = np.nanstd(array_tmp, axis=0)  # stddev 
                var_array_err[iseason, :] = data0 / (math.sqrt(narray))
                var_array[iseason, :] = np.nanmean(array_tmp, axis=0)
        except Exception as e:
            print(f"Error processing observation data for {variables[ivar]}: {e}")
            var_array = np.empty([nseasons, 24]) * np.nan
            var_array_err = np.empty([nseasons, 24]) * np.nan
            
        #==========================
        # Seasons: for models
        #==========================
        try:
            # Extract variable from the test dataset
            if variables[ivar] in test_ds:
                var_mod = test_ds[variables[ivar]].values
            else:
                print(f"Variable {variables[ivar]} not found in test model dataset. Skipping model processing.")
                var_mod_array = np.empty([nseasons, 8]) * np.nan
                var_mod_array_err = np.empty([nseasons, 8]) * np.nan
                continue
                
            years_mod = list(range(2003, 2015))
            nyears_mod = len(years_mod)

            # Process the data with our xarray-compatible function - always use 8-hour resolution for model data
            nhour_mod = 8  # Model data always has 8 hours (3-hourly)
            var_mod_seasons = get_diurnal_cycle_seasons_xr(var_mod, seasons, years_mod, nhour=nhour_mod)
            
            # Verify the shape of the output data matches what we expect
            if var_mod_seasons.shape[3] != nhour_mod:
                print(f"Warning: Expected {nhour_mod} hours in model data, but got {var_mod_seasons.shape[3]}. Adjusting output shape.")
                # If we got different shape than expected, create a dummy array of correct shape
                var_mod_array = np.empty([nseasons, nhour_mod]) * np.nan
                var_mod_array_err = np.empty([nseasons, nhour_mod]) * np.nan
                continue  # Skip further processing for this variable
            
            narray = nyears_mod * 365
            var_mod_seasons1 = np.empty([nseasons, narray, nhour_mod]) * np.nan
            var_mod_array_err = np.empty([nseasons, nhour_mod]) * np.nan
            var_mod_array = np.empty([nseasons, nhour_mod]) * np.nan
            
            for iseason in range(nseasons):
                for iyear in range(nyears_mod):
                    for iday in range(365):
                        var_mod_seasons1[iseason, 365*iyear+iday, :] = var_mod_seasons[iyear, iseason, iday, :]
     
                array_tmp = var_mod_seasons1[iseason, :, :]
                data0 = np.nanstd(array_tmp, axis=0)  # stddev
                var_mod_array_err[iseason, :] = data0 / (math.sqrt(narray))
                var_mod_array[iseason, :] = np.nanmean(array_tmp, axis=0)
        except Exception as e:
            print(f"Error processing model data for {variables[ivar]}: {e}")
            var_mod_array_err = np.empty([nseasons, 8]) * np.nan
            var_mod_array = np.empty([nseasons, 8]) * np.nan

        #==========================================================================
        # Plotting: Diurnal cycle (daytime)
        #==========================================================================
        for iseason in range(nseasons):
            fig = plt.figure(figsize=[8, 4], dpi=100)
            xax = np.array([x for x in range(26)]) - 0.5
            y_data = np.empty([26]) * np.nan
            y_data[0:19] = var_array[iseason, 5:24]  
            y_data[19:26] = var_array[iseason, 0:7]
         
            e_data = np.empty([26]) * np.nan
            e_data[0:19] = var_array_err[iseason, 5:24]
            e_data[19:26] = var_array_err[iseason, 0:7]
            plt.errorbar(xax, y_data, e_data, color='black', label='OBS', linewidth=2)

            
            if variables[ivar] == 'SH' or variables[ivar] == 'LH':
                xax1 = np.array([x for x in range(10)]) * 3 - 1.5
            else:
                xax1 = np.array([x for x in range(10)]) * 3 - 3.0
            y1_data = np.empty([10]) * np.nan
            y1_data[0:7] = var_mod_array[iseason, 1:8]
            y1_data[7:10] = var_mod_array[iseason, 0:3]

            e1_data = np.empty([10]) * np.nan
            e1_data[0:7] = var_mod_array_err[iseason, 1:8]
            e1_data[7:10] = var_mod_array_err[iseason, 0:3]
            plt.errorbar(xax1, y1_data, e1_data, color='red', label='MOD', linewidth=2)

            plt.ylabel(units[ivar], fontsize=12)
            plt.title(f"{variables[ivar]} ({seasons[iseason]})", fontsize=14)
            plt.xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
                ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.xlabel('LST (hour)', fontsize=12)
            plt.xlim([-0.1, 24.1])
            if variables[ivar] == 'pbl':
                plt.xlim([7.4, 17.6])
            plt.legend()
            fig_path = os.path.join(output_path, 'figures', sites[0], 
                                   f"Diurnal_cycle_{seasons[iseason]}_{variables[ivar]}_{sites[0]}.png")
            plt.savefig(fig_path)
            plt.close()
            
    # Close datasets
    if 'test_ds' in locals():
        test_ds.close()
    if 'obs_ds' in locals():
        obs_ds.close()