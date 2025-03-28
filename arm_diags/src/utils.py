#===========================================================================================================================
# Functions for calculate annual/seasonal cycle from monthly data -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### Add the array treatment: filled the output masked (missing) value with numpy NaN
    # ### to avoid the issue of plotting masked value as 0 value in the plotting code
    # ---------------------------------------------------------------------------------------
# V4 Development
    # ---------------------------------------------------------------------------------------
    # 2024
    # ### Replaced cdms2/cdutil with xarray and xcdat for modern compatibility (similar to E3SM Diagnostics)
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================

import numpy as np
import pandas as pd
import xarray as xr
import xcdat
import calendar
from copy import deepcopy

def climo(var, season):
    """
    Compute climatology for the given season using xarray/xcdat.
    
    Args:
        var: xarray.DataArray or numpy array
        season: Season to compute climatology for ('ANN', 'DJF', 'MAM', 'JJA', 'SON',
               'ANNUALCYCLE', 'SEASONALCYCLE', or month number '01'-'12')
        
    Returns:
        numpy array of climatology values
    """
    # Convert to xarray DataArray if needed
    if not isinstance(var, xr.DataArray):
        # For backward compatibility with cdms2
        if hasattr(var, 'getValue'):
            values = var.getValue()
            var_id = getattr(var, 'id', 'unknown')
        else:
            values = np.array(var)
            var_id = 'unknown'
        
        # Create a simple DataArray with time dimension
        da = xr.DataArray(
            values,
            dims=['time'] + [f'dim_{i}' for i in range(values.ndim - 1)],
            name=var_id
        )
        da.attrs['id'] = var_id
    else:
        da = var
        var_id = da.name
    
    # Convert to xcdat.Dataset for temporal operations
    ds = xcdat.Dataset({"var": da})
    
    # Compute climatology based on season
    if season == 'ANNUALCYCLE':
        # Return monthly climatology
        result = ds.var.temporal.climatology(freq="month").values
    elif season == 'SEASONALCYCLE':
        # Return seasonal climatology
        result = np.array([
            ds.var.temporal.climatology(freq="season", season="DJF").values,
            ds.var.temporal.climatology(freq="season", season="MAM").values,
            ds.var.temporal.climatology(freq="season", season="JJA").values,
            ds.var.temporal.climatology(freq="season", season="SON").values
        ])
    elif season in ['DJF', 'MAM', 'JJA', 'SON']:
        # Return specific seasonal climatology
        result = ds.var.temporal.climatology(freq="season", season=season).values
    elif season == 'ANN':
        # Return annual climatology
        result = ds.var.temporal.climatology(freq="year").values
    elif season in [str(i).zfill(2) for i in range(1, 13)]:
        # Return specific month's climatology
        month_num = int(season)
        result = ds.var.sel(time=ds.var.time.dt.month == month_num).mean('time').values
    else:
        raise ValueError(f"Unknown season: {season}")
        
    # Apply unit conversions
    if var_id == 'tas':
        result = result - 273.15
    if var_id == 'pr':
        result = result * 3600.0 * 24.0
    
    return result
    
def get_diurnal_cycle_seasons(var, seasons, years):
    """
    Extract diurnal cycle data for specific seasons and years.
    
    Args:
        var: xarray.DataArray with hourly or sub-daily time resolution
        seasons: List of season names
        years: List of years to extract
        
    Returns:
        numpy array with dimensions [year, season, day, hour]
    """
    # Convert to xarray if needed
    if not isinstance(var, xr.DataArray):
        if hasattr(var, 'getValue'):
            # Convert from cdms2
            values = var.getValue()
            times = var.getAxis(0)
            
            # Create a time axis
            if hasattr(times, 'asComponentTime'):
                # Convert cdms2 time to datetime
                time_values = pd.DatetimeIndex([
                    pd.Timestamp(t.strftime('%Y-%m-%d %H:%M:%S'))
                    for t in times.asComponentTime()
                ])
            else:
                # Use simple time coordinates
                time_values = pd.date_range(
                    start=f"{years[0]}-01-01",
                    periods=values.shape[0],
                    freq='H'
                )
                
            da = xr.DataArray(
                values,
                dims=['time'] + [f'dim_{i}' for i in range(values.ndim - 1)],
                coords={'time': time_values}
            )
        else:
            # Handle numpy array
            values = np.array(var)
            time_values = pd.date_range(
                start=f"{years[0]}-01-01",
                periods=values.shape[0],
                freq='H'
            )
            
            da = xr.DataArray(
                values,
                dims=['time'] + [f'dim_{i}' for i in range(values.ndim - 1)],
                coords={'time': time_values}
            )
    else:
        da = var
        
    # Determine time resolution
    time_diff = (da.time[1] - da.time[0]).values
    time_diff_hours = pd.Timedelta(time_diff).total_seconds() / 3600
    nhour = int(24 / time_diff_hours) if time_diff_hours <= 24 else 1
    
    # Prepare result array
    result = np.full((len(years), len(seasons), 365, nhour), np.nan)
    
    # Process each year and season
    for iyear, year in enumerate(years):
        year_data = da.sel(time=slice(f"{year}-01-01", f"{year}-12-31"))
        is_leap = calendar.isleap(int(year))
        
        for iseason, season in enumerate(seasons):
            if season == 'ANN':
                # Process all days in the year (up to 365)
                # Group by day of year to handle different time frequencies
                grouped = year_data.groupby('time.dayofyear')
                
                for day_idx, (day, day_data) in enumerate(grouped):
                    if day_idx >= 365:  # Skip leap day if present
                        continue
                        
                    # Group by hour within day
                    day_by_hour = day_data.groupby('time.hour')
                    
                    # Fill the result array with hourly data
                    for hour_idx, (hour, hour_data) in enumerate(day_by_hour):
                        if hour_idx < nhour:
                            result[iyear, iseason, day_idx, hour_idx] = hour_data.mean().values
            else:
                # Process seasonal data
                if season == 'DJF':
                    season_data = da.sel(
                        time=(da.time.dt.month.isin([12, 1, 2])) & 
                             (da.time.dt.year == year)
                    )
                elif season == 'MAM':
                    season_data = da.sel(
                        time=(da.time.dt.month.isin([3, 4, 5])) & 
                             (da.time.dt.year == year)
                    )
                elif season == 'JJA':
                    season_data = da.sel(
                        time=(da.time.dt.month.isin([6, 7, 8])) & 
                             (da.time.dt.year == year)
                    )
                elif season == 'SON':
                    season_data = da.sel(
                        time=(da.time.dt.month.isin([9, 10, 11])) & 
                             (da.time.dt.year == year)
                    )
                else:
                    continue
                
                # Get day index offset for the season
                if season == 'MAM':
                    day_offset = 60 if is_leap else 59
                elif season == 'JJA':
                    day_offset = 152 if is_leap else 151
                elif season == 'SON':
                    day_offset = 244 if is_leap else 243
                elif season == 'DJF':
                    day_offset = 335 if is_leap else 334
                else:
                    day_offset = 0
                
                # Group by day and hour
                season_by_day = season_data.groupby('time.dayofyear')
                
                # Fill the result array
                for rel_day_idx, (day, day_data) in enumerate(season_by_day):
                    if rel_day_idx >= 90:  # Use at most 90 days for each season
                        break
                        
                    # Group by hour
                    day_by_hour = day_data.groupby('time.hour')
                    
                    for hour_idx, (hour, hour_data) in enumerate(day_by_hour):
                        if hour_idx < nhour:
                            result[iyear, iseason, rel_day_idx, hour_idx] = hour_data.mean().values
    
    return result