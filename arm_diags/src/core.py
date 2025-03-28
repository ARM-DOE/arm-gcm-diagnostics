"""
Core utilities for ARM Diagnostics.

This module provides core utility functions for common operations
in the ARM Diagnostics package, similar to E3SM Diagnostics approach.
"""

import os
import numpy as np
import xarray as xr
import xcdat
import pandas as pd
import warnings

def climo(da, season):
    """
    Calculate climatology for a specific season.
    
    This function replaces the original cdutil-based climo function with
    an xarray/xcdat implementation.
    
    Args:
        da: xarray.DataArray with time dimension
        season: Season name ('ANN', 'DJF', 'MAM', 'JJA', 'SON', 'ANNUALCYCLE', 'SEASONALCYCLE')
            or month number as string ('01'-'12')
            
    Returns:
        Climatology as numpy array
    """
    # Ensure we're working with a DataArray
    if not isinstance(da, xr.DataArray):
        raise ValueError("Input must be an xarray.DataArray")
    
    # Add to xcdat.Dataset for temporal operations
    ds = xcdat.Dataset({"var": da})
    
    # Process by season type
    if season == 'ANNUALCYCLE':
        # Monthly climatology
        result = ds.var.temporal.climatology(freq="month")
    elif season == 'SEASONALCYCLE':
        # Seasonal climatology
        result = xr.concat([
            ds.var.temporal.climatology(freq="season", season="DJF"),
            ds.var.temporal.climatology(freq="season", season="MAM"),
            ds.var.temporal.climatology(freq="season", season="JJA"),
            ds.var.temporal.climatology(freq="season", season="SON")
        ], dim=pd.Index(["DJF", "MAM", "JJA", "SON"], name="season"))
    elif season == 'ANN':
        # Annual mean
        result = ds.var.temporal.climatology(freq="year")
    elif season in ['DJF', 'MAM', 'JJA', 'SON']:
        # Specific season
        result = ds.var.temporal.climatology(freq="season", season=season)
    elif season in [f"{m:02d}" for m in range(1, 13)]:
        # Specific month
        month = int(season)
        result = ds.var.sel(time=ds.var.time.dt.month == month).mean(dim="time")
    else:
        raise ValueError(f"Unknown season: {season}")
    
    # Apply unit conversions if needed (matching original behavior)
    var_id = da.attrs.get('id', '')
    
    if var_id == 'tas':
        # Convert from K to C
        result = result - 273.15
    elif var_id == 'pr':
        # Convert precipitation units - scale by 24 hours and 3600 seconds
        result = result * 3600.0 * 24.0
    
    # Convert to numpy array
    if hasattr(result, 'values'):
        result = result.values
    
    return result


def get_diurnal_cycle(da, seasons, years):
    """
    Extract diurnal cycle data for specific seasons and years.
    
    Args:
        da: xarray.DataArray with sub-daily time resolution
        seasons: List of season names ('ANN', 'DJF', 'MAM', 'JJA', 'SON')
        years: List of years to process
        
    Returns:
        numpy array with dimensions [year, season, day, hour]
    """
    # Ensure we're working with a DataArray
    if not isinstance(da, xr.DataArray):
        raise ValueError("Input must be an xarray.DataArray")
    
    # Determine time resolution
    if len(da.time) <= 1:
        raise ValueError("DataArray must have multiple time points")
    
    time_diff = (da.time[1] - da.time[0]).values
    time_diff_hours = pd.Timedelta(time_diff).total_seconds() / 3600
    nhour = max(1, int(24 / time_diff_hours))
    
    # Create output array
    result = np.full((len(years), len(seasons), 365, nhour), np.nan)
    
    # Process each year
    for iyear, year in enumerate(years):
        # Select data for this year
        year_data = da.sel(time=da.time.dt.year == year)
        
        for iseason, season in enumerate(seasons):
            if season == 'ANN':
                # Process all days (up to 365)
                days = year_data.groupby('time.dayofyear')
                
                for day_idx, (day, day_data) in enumerate(days):
                    if day_idx >= 365:  # Skip leap day
                        continue
                    
                    # Process hours within day
                    hours = day_data.groupby('time.hour')
                    for hour_idx, (hour, hour_data) in enumerate(hours):
                        if hour_idx < nhour:
                            result[iyear, iseason, day_idx, hour_idx] = hour_data.mean().values
            else:
                # Process seasonal data
                if season == 'DJF':
                    month_filter = [12, 1, 2]
                elif season == 'MAM':
                    month_filter = [3, 4, 5]
                elif season == 'JJA':
                    month_filter = [6, 7, 8]
                elif season == 'SON':
                    month_filter = [9, 10, 11]
                else:
                    continue
                
                # Select data for this season
                season_data = year_data.sel(time=year_data.time.dt.month.isin(month_filter))
                days = season_data.groupby('time.dayofyear')
                
                # Fill days sequentially for this season
                for day_idx, (day, day_data) in enumerate(days):
                    if day_idx >= 90:  # Limit to 90 days per season
                        break
                    
                    # Process hours within day
                    hours = day_data.groupby('time.hour')
                    for hour_idx, (hour, hour_data) in enumerate(hours):
                        if hour_idx < nhour:
                            result[iyear, iseason, day_idx, hour_idx] = hour_data.mean().values
    
    return result


def var_annual_cycle(da, seasons):
    """
    Calculate annual cycle climatology.
    
    Args:
        da: xarray.DataArray with time dimension
        seasons: List of seasons or months
        
    Returns:
        Monthly climatology as xarray.DataArray
    """
    # Ensure we're working with a DataArray with time coordinates
    if not isinstance(da, xr.DataArray) or 'time' not in da.coords:
        raise ValueError("Input must be an xarray.DataArray with time coordinate")
    
    # Create xcdat.Dataset for temporal operations
    ds = xcdat.Dataset({"var": da})
    
    # Calculate monthly climatology
    result = ds.var.temporal.climatology(freq="month")
    
    # Apply unit conversions if needed
    var_id = da.attrs.get('id', '')
    
    if var_id == 'tas':
        result = result - 273.15
    elif var_id == 'pr':
        result = result * 3600.0 * 24.0
    
    return result