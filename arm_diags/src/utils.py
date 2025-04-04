#===========================================================================================================================
# Functions for calculate annual/seasonal cycle from monthly data
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### Add the array treatment: filled the output masked (missing) value with numpy NaN
    # ### to avoid the issue of plotting masked value as 0 value in the plotting code
    # ---------------------------------------------------------------------------------------
# V4 Update
    # ---------------------------------------------------------------------------------------
    # Xarray Refactoring - Apr2025
    # ### Replace cdms2/cdutil/MV2 with xarray and numpy implementations
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================

import numpy as np
import numpy.ma as ma
import xarray as xr
import pdb
from copy import deepcopy
import calendar

def climo(var, season):
    """
    Compute the climatology for var for the given season using xarray.
    
    Args:
        var (xarray.DataArray): The variable to compute climatology for
        season (str or list): Season to compute climatology for
            'ANNUALCYCLE' for all months
            'SEASONALCYCLE' for seasonal means (DJF, MAM, JJA, SON)
            or a specific season like 'JJA'
    
    Returns:
        numpy.ndarray: Climatology values for the specified season(s)
    """
    season_idx = {
        '01': [1,0,0,0,0,0,0,0,0,0,0,0],
        '02': [0,1,0,0,0,0,0,0,0,0,0,0],
        '03': [0,0,1,0,0,0,0,0,0,0,0,0],
        '04': [0,0,0,1,0,0,0,0,0,0,0,0],
        '05': [0,0,0,0,1,0,0,0,0,0,0,0],
        '06': [0,0,0,0,0,1,0,0,0,0,0,0],
        '07': [0,0,0,0,0,0,1,0,0,0,0,0],
        '08': [0,0,0,0,0,0,0,1,0,0,0,0],
        '09': [0,0,0,0,0,0,0,0,1,0,0,0],
        '10': [0,0,0,0,0,0,0,0,0,1,0,0],
        '11': [0,0,0,0,0,0,0,0,0,0,1,0],
        '12': [0,0,0,0,0,0,0,0,0,0,0,1],
        'DJF':[1,1,0,0,0,0,0,0,0,0,0,1],
        'MAM':[0,0,1,1,1,0,0,0,0,0,0,0],
        'JJA':[0,0,0,0,0,1,1,1,0,0,0,0],
        'SON':[0,0,0,0,0,0,0,0,1,1,1,0],
        'ANN':[1,1,1,1,1,1,1,1,1,1,1,1],
    }

    # Check if 'time' coordinate exists
    if not isinstance(var, xr.DataArray) or 'time' not in var.dims:
        return var.values if hasattr(var, 'values') else var

    # Define the cycle based on the season parameter
    if season == 'ANNUALCYCLE':
        cycle = ['01','02','03','04','05','06','07','08','09','10','11','12']
    elif season == 'SEASONALCYCLE':
        cycle = ['DJF','MAM','JJA','SON']
    else:
        cycle = season if isinstance(season, list) else [season]
    
    # Extract month information
    try:
        months = var.time.dt.month.values
    except:
        # If we can't determine months, return original variable
        return var.values
    
    # Calculate climatology for each cycle
    ncycle = len(cycle)
    climo_values = np.zeros(ncycle)
    
    for n in range(ncycle):
        # Create mask for current season
        mask = np.zeros_like(months, dtype=bool)
        for i, m in enumerate(months):
            if m <= 12 and season_idx[cycle[n]][m-1] == 1:
                mask[i] = True
        
        # Skip if no data for this season
        if not np.any(mask):
            climo_values[n] = np.nan
            continue
            
        # Calculate mean for the season
        seasonal_data = var.values[mask]
        climo_values[n] = np.nanmean(seasonal_data)
    
    # Apply unit conversions if needed
    var_name = var.name if hasattr(var, 'name') else None
    
    if var_name == 'tas':
        climo_values = climo_values - 273.15
    
    if var_name == 'pr':
        climo_values = climo_values * 3600.0 * 24.0
    
    return climo_values

def get_diurnal_cycle_seasons(var, seasons, years, nhour=None):
    """
    Get seasonal data for diurnal cycle analysis using xarray.
    
    Args:
        var (xarray.DataArray): The variable to analyze
        seasons (list): List of seasons to analyze
        years (list): List of years to analyze
        nhour (int, optional): Number of hours per day (8 for 3-hourly, 24 for hourly)
        
    Returns:
        numpy.ndarray: Seasonal data with shape [nyears, nseasons, 365, nhour]
    """
    nyears = len(years)
    nseasons = len(seasons)
    t0 = 0
    
    # If nhour is not provided, try to determine from data
    if nhour is None:
        if 'time' in var.dims and len(var.time) > 1:
            try:
                time_diff = np.diff(var.time.values)[0]
                if hasattr(time_diff, 'astype'):
                    hours = time_diff.astype('timedelta64[h]').astype(int)
                    if hours == 1:
                        nhour = 24  # hourly data
                    elif hours == 3:
                        nhour = 8   # 3-hourly data
                    else:
                        nhour = 24  # default to hourly
                else:
                    nhour = 24
            except:
                nhour = 24
        else:
            nhour = 24
    
    # Get values from DataArray
    var_values = var.values if hasattr(var, 'values') else np.array(var)
    
    # Initialize the output array
    var_seasons = np.zeros([nyears, nseasons, 365, nhour]) * np.nan
    
    for iyear in range(nyears):
        if calendar.isleap(int(years[iyear])):
            nday = 366
        else:
            nday = 365
            
        ntime = int(nday * nhour)
        
        # Extract data for the current year
        if t0 + ntime <= len(var_values):
            var1 = var_values[t0:t0+ntime]
            # Create an extended array by concatenating the data with itself
            var1_ext = np.concatenate((var1, var1), axis=0)
            t0 = t0 + ntime
        else:
            # Not enough data for this year
            continue

        for iseason in range(nseasons):
            if seasons[iseason] == 'ANN':
                # For annual data, use up to 365 days
                length = min(nday, 365) * nhour
                var_seasons0 = var1[0:length]
                try:
                    var_seasons1 = np.reshape(var_seasons0, (min(nday, 365), nhour))
                    var_seasons[iyear, iseason, :min(nday, 365), :] = var_seasons1
                except ValueError:
                    # Skip if reshape fails
                    continue
            else:
                # For seasonal data, determine starting day
                if seasons[iseason] == 'MAM':
                    if nday == 366: t1 = 60
                    else: t1 = 59
                elif seasons[iseason] == 'JJA':
                    if nday == 366: t1 = 152
                    else: t1 = 151
                elif seasons[iseason] == 'SON':
                    if nday == 366: t1 = 244
                    else: t1 = 243
                elif seasons[iseason] == 'DJF':
                    if nday == 366: t1 = 335
                    else: t1 = 334
                else:
                    # Skip unknown season
                    continue
                
                # Extract 90 days of data for the season
                var_seasons0 = var1_ext[int(t1*nhour):int(t1*nhour)+90*nhour]
                try:
                    var_seasons1 = np.reshape(var_seasons0, (90, nhour))
                    var_seasons[iyear, iseason, 0:90, :] = var_seasons1
                except ValueError:
                    # Skip if reshape fails
                    continue

    return var_seasons