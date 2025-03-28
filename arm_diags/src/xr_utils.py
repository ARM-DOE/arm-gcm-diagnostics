"""
Utility functions to replace cdms2/cdutil functionality with xarray.

This module provides drop-in replacements for common CDMS operations using xarray.
It helps with the transition from cdms2/cdutil to xarray for ARM Diagnostics.
"""

import os
import re
import numpy as np
import pandas as pd
import xarray as xr
import calendar
import datetime


def open_dataset(filename, variable_id=None):
    """
    Open a netCDF file as an xarray dataset.
    
    Args:
        filename: Path to the netCDF file
        variable_id: Optional variable ID to extract
        
    Returns:
        xarray.Dataset or xarray.DataArray if variable_id is specified
    """
    ds = xr.open_dataset(filename)
    
    # If a specific variable is requested, return it as a DataArray
    if variable_id is not None:
        # Find the actual variable name in the dataset
        # (handle case differences and similar naming conventions)
        varname = _find_variable_name(ds, variable_id)
        if varname:
            return ds[varname]
        else:
            raise ValueError(f"Variable {variable_id} not found in {filename}")
    
    return ds


def _find_variable_name(ds, var_id):
    """Find the actual variable name in the dataset that matches the requested ID."""
    # Try exact match first
    if var_id in ds.variables:
        return var_id
    
    # Try case-insensitive match
    var_id_lower = var_id.lower()
    for var in ds.variables:
        if var.lower() == var_id_lower:
            return var
    
    # Try with standard name
    for var in ds.variables:
        if hasattr(ds[var], 'standard_name') and ds[var].standard_name == var_id:
            return var
    
    return None


def set_time_bounds_monthly(ds):
    """
    Add monthly time bounds to a dataset or data array.
    
    Args:
        ds: xarray.Dataset or xarray.DataArray
        
    Returns:
        Modified dataset or data array with time bounds
    """
    if not isinstance(ds.time.values[0], (np.datetime64, datetime.datetime, pd.Timestamp)):
        # Try to convert numeric time to datetime if needed
        # This is a simplistic approach - may need customization based on data
        if 'units' in ds.time.attrs and 'since' in ds.time.attrs['units']:
            # Extract the reference date from the units string
            time_units = ds.time.attrs['units']
            match = re.search(r'since\s+(\d{4}-\d{1,2}-\d{1,2})', time_units)
            if match:
                ref_date = match.group(1)
                # Try to make this a proper CF-compliant time axis
                ds = ds.assign_coords(time=pd.date_range(
                    start=ref_date, 
                    periods=len(ds.time), 
                    freq=pd.infer_freq(ds.time.values)
                ))
    
    # Create time bounds
    time_bounds = []
    for t in ds.time.values:
        t_datetime = pd.Timestamp(t)
        start_month = datetime.datetime(t_datetime.year, t_datetime.month, 1)
        
        # Find the last day of the month
        if t_datetime.month == 12:
            last_day = datetime.datetime(t_datetime.year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            last_day = datetime.datetime(t_datetime.year, t_datetime.month + 1, 1) - datetime.timedelta(days=1)
        
        end_month = datetime.datetime(last_day.year, last_day.month, last_day.day, 23, 59, 59)
        time_bounds.append([start_month, end_month])
    
    # Add the bounds to the dataset
    bounds_da = xr.DataArray(
        time_bounds,
        dims=['time', 'bnds'],
        coords={'time': ds.time}
    )
    
    if isinstance(ds, xr.Dataset):
        ds = ds.assign(time_bnds=bounds_da)
        ds.time.attrs['bounds'] = 'time_bnds'
    else:  # DataArray
        # Create a new dataset with the original data array and the bounds
        new_ds = xr.Dataset({ds.name: ds})
        new_ds = new_ds.assign(time_bnds=bounds_da)
        new_ds.time.attrs['bounds'] = 'time_bnds'
        ds = new_ds[ds.name]
        ds.attrs['bounds'] = 'time_bnds'
    
    return ds


def get_time_weights(da):
    """
    Calculate time weights for temporal averaging.
    
    Args:
        da: xarray.DataArray with time dimension
        
    Returns:
        xarray.DataArray of weights
    """
    # If time bounds exist, use them to calculate weights
    if 'time_bnds' in da.coords or 'time_bnds' in da.variables:
        time_bnds = da['time_bnds'] if 'time_bnds' in da.variables else da.coords['time_bnds']
        # Convert to datetime if not already
        if not np.issubdtype(time_bnds.dtype, np.datetime64):
            # This is a simplistic conversion - may need customization
            time_units = da.time.attrs.get('units', '')
            if 'since' in time_units:
                match = re.search(r'since\s+(\d{4}-\d{1,2}-\d{1,2})', time_units)
                if match:
                    ref_date = pd.Timestamp(match.group(1))
                    time_bnds = ref_date + pd.to_timedelta(time_bnds.values, unit='D')
        
        # Calculate the time difference in days
        delta_t = (time_bnds[:, 1] - time_bnds[:, 0]) / np.timedelta64(1, 'D')
        weights = xr.DataArray(delta_t, coords=[da.time], dims=['time'])
    else:
        # No bounds available, use equal weights
        weights = xr.ones_like(da.time)
    
    # Normalize weights
    weights = weights / weights.sum()
    return weights


def climatology(da, season='ANN'):
    """
    Compute climatology for a specific season.
    
    Args:
        da: xarray.DataArray with time dimension
        season: String indicating the season ('ANN', 'DJF', 'MAM', 'JJA', 'SON', 
                'ANNUALCYCLE', 'SEASONALCYCLE', or month number '01'-'12')
                
    Returns:
        xarray.DataArray with climatological average
    """
    # Ensure we have time bounds for proper weighted averaging
    if 'time_bnds' not in da.coords and 'time_bnds' not in da.variables:
        da = set_time_bounds_monthly(da)
    
    # Define season indices
    season_idx = {
        '01': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        '02': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        '03': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        '04': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        '05': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        '06': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        '07': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        '08': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        '09': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        '10': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        '11': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        '12': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        'DJF': [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        'MAM': [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        'JJA': [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        'SON': [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        'ANN': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    }
    
    # Determine the cycle based on the season
    if season == 'ANNUALCYCLE':
        cycle = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    elif season == 'SEASONALCYCLE':
        cycle = ['DJF', 'MAM', 'JJA', 'SON']
    else:
        cycle = [season]
    
    # Extract month information from the time coordinate
    time_months = xr.DataArray(
        [dt.month for dt in pd.DatetimeIndex(da.time.values)],
        dims='time',
        coords={'time': da.time}
    )
    
    # Process each season in the cycle
    result_list = []
    for s in cycle:
        # Create a mask for the current season
        s_idx = np.array(season_idx[s])
        mask = np.zeros_like(time_months.values, dtype=bool)
        for i, month in enumerate(range(1, 13)):
            if s_idx[i]:
                mask = mask | (time_months == month)
        
        # Apply the mask and calculate weighted average
        if np.any(mask):
            da_season = da.isel(time=mask)
            weights = get_time_weights(da_season)
            avg = (da_season * weights).sum(dim='time')
            result_list.append(avg)
        else:
            # No data for this season
            avg = xr.full_like(da.isel(time=0), np.nan)
            result_list.append(avg)
    
    # Stack the results along a new dimension
    if len(result_list) > 1:
        result = xr.concat(result_list, dim=pd.Index(cycle, name='season'))
    else:
        result = result_list[0]
    
    # Apply units conversions for specific variables (same as in original utils.py)
    if 'id' in da.attrs and da.attrs['id'] == 'tas':
        result = result - 273.15
    elif 'id' in da.attrs and da.attrs['id'] == 'pr':
        result = result * 3600.0 * 24.0
    
    return result


def annual_cycle_climatology(da):
    """
    Calculate the annual cycle climatology.
    
    Similar to cdutil.ANNUALCYCLE.climatology().
    
    Args:
        da: xarray.DataArray with time dimension
        
    Returns:
        xarray.DataArray with climatological monthly means
    """
    # Ensure we have time bounds for proper weighted averaging
    if 'time_bnds' not in da.coords and 'time_bnds' not in da.variables:
        da = set_time_bounds_monthly(da)
    
    # Group by month and calculate weighted averages
    monthly_data = da.groupby('time.month')
    
    # Calculate weights for each month's data
    month_weights = []
    for month, group in monthly_data:
        weights = get_time_weights(group)
        month_weights.append((month, weights))
    
    # Apply weights and calculate monthly means
    monthly_means = []
    for month, group in monthly_data:
        # Find weights for this month
        for m, w in month_weights:
            if m == month:
                weights = w
                break
        else:
            # No weights found, use equal weighting
            weights = xr.ones_like(group.time) / len(group.time)
        
        # Calculate weighted average
        mean = (group * weights).sum(dim='time')
        monthly_means.append(mean)
    
    # Combine into a single DataArray with month dimension
    result = xr.concat(monthly_means, dim=pd.Index(range(1, 13), name='month'))
    
    # Apply units conversions for specific variables
    if 'id' in da.attrs and da.attrs['id'] == 'tas':
        result = result - 273.15
    elif 'id' in da.attrs and da.attrs['id'] == 'pr':
        result = result * 3600.0 * 24.0
    
    return result


def get_diurnal_cycle_seasons(da, seasons, years):
    """
    Extract diurnal cycle data for specific seasons and years.
    
    Args:
        da: xarray.DataArray with time dimension
        seasons: List of season names
        years: List of years to extract
        
    Returns:
        xarray.DataArray with dimensions [year, season, day, hour]
    """
    # Convert to DataArray if it's a Dataset
    if isinstance(da, xr.Dataset):
        if len(da.data_vars) == 1:
            da = next(iter(da.data_vars.values()))
        else:
            raise ValueError("Dataset contains multiple variables. Please specify a single variable.")
    
    # Get time index
    time_idx = pd.DatetimeIndex(da.time.values)
    
    # Determine time resolution (hours between time steps)
    time_diff = (time_idx[1] - time_idx[0]).total_seconds() / 3600.0
    if time_diff == 1:
        nhour = 24
    elif time_diff == 3:
        nhour = 8
    else:
        nhour = int(24 / time_diff)
    
    # Create empty array for results
    result = np.full((len(years), len(seasons), 365, nhour), np.nan)
    
    # Current time index position
    t0 = 0
    
    # Process each year
    for iyear, year in enumerate(years):
        # Determine if it's a leap year
        is_leap = calendar.isleap(int(year))
        nday = 366 if is_leap else 365
        
        # Calculate number of time steps for this year
        ntime = int(nday * nhour)
        
        # Extract data for this year
        year_data = da.isel(time=slice(t0, t0 + ntime)).values
        
        # Extend data by repeating (for handling season boundaries)
        year_data_ext = np.concatenate((year_data, year_data), axis=0)
        
        # Update time index position
        t0 += ntime
        
        # Process each season
        for iseason, season in enumerate(seasons):
            if season == 'ANN':
                # For annual, use all days (limited to 365 for consistency)
                length = 365 * nhour
                season_data = year_data[:length]
                season_data_reshaped = season_data.reshape(365, nhour)
                result[iyear, iseason, :, :] = season_data_reshaped
            else:
                # Get starting day of season
                if season == 'MAM':
                    t1 = 60 if is_leap else 59
                elif season == 'JJA':
                    t1 = 152 if is_leap else 151
                elif season == 'SON':
                    t1 = 244 if is_leap else 243
                elif season == 'DJF':
                    t1 = 335 if is_leap else 334
                else:
                    continue  # Skip unknown seasons
                
                # Extract 90 days of data starting from t1
                season_data = year_data_ext[int(t1 * nhour):int(t1 * nhour) + 90 * nhour]
                season_data_reshaped = season_data.reshape(90, nhour)
                result[iyear, iseason, 0:90, :] = season_data_reshaped
    
    # Convert to xarray DataArray with proper dimensions
    coords = {
        'year': years,
        'season': seasons,
        'day': np.arange(365),
        'hour': np.arange(nhour)
    }
    result_da = xr.DataArray(
        result,
        dims=['year', 'season', 'day', 'hour'],
        coords=coords,
        name=da.name
    )
    
    # Copy attributes
    result_da.attrs.update(da.attrs)
    
    return result_da