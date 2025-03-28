"""
Data utilities for ARM Diagnostics using xarray/xcdat.

This module provides data loading and preprocessing functions
using xarray and xcdat for the ARM Diagnostics package.
"""

import os
import numpy as np
import pandas as pd
import xarray as xr
import xcdat
import warnings

def open_dataset(filename, variable_id=None):
    """
    Open a netCDF file as an xarray dataset or data array.
    
    Similar to cdms2.open() but using xarray.
    
    Args:
        filename: Path to the netCDF file
        variable_id: Optional variable ID to extract
        
    Returns:
        xarray.Dataset or xarray.DataArray if variable_id is specified
    """
    # Check if file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    try:
        # Try using xcdat's open_dataset for better CF compliance
        ds = xcdat.open_dataset(filename)
    except:
        # Fall back to standard xarray
        try:
            ds = xr.open_dataset(filename)
        except Exception as e:
            raise IOError(f"Error opening file {filename}: {e}")
    
    # Return the dataset if no variable is specified
    if variable_id is None:
        return ds
    
    # Find the actual variable name (case-insensitive)
    found_var = None
    for var_name in ds.data_vars:
        if var_name.lower() == variable_id.lower():
            found_var = var_name
            break
    
    # Try standard_name if not found by name
    if found_var is None:
        for var_name, var in ds.data_vars.items():
            if hasattr(var, 'standard_name') and var.standard_name == variable_id:
                found_var = var_name
                break
                
    # If we found a matching variable, return it
    if found_var is not None:
        da = ds[found_var]
        # Store original variable ID in attributes
        da.attrs['id'] = variable_id
        return da
    else:
        raise ValueError(f"Variable {variable_id} not found in {filename}")


def variable_from_dataset(ds, variable_id):
    """
    Extract a variable from a dataset.
    
    Args:
        ds: xarray.Dataset
        variable_id: Variable ID to extract
        
    Returns:
        xarray.DataArray
    """
    # Find the variable (case-insensitive)
    for var_name in ds.data_vars:
        if var_name.lower() == variable_id.lower():
            da = ds[var_name]
            da.attrs['id'] = variable_id
            return da
    
    # Try standard_name if not found by name
    for var_name, var in ds.data_vars.items():
        if hasattr(var, 'standard_name') and var.standard_name == variable_id:
            da = ds[var_name]
            da.attrs['id'] = variable_id
            return da
            
    raise ValueError(f"Variable {variable_id} not found in dataset")


def time_slice(data, start_time=None, end_time=None):
    """
    Extract a time slice from a dataset or data array.
    
    Args:
        data: xarray.Dataset or xarray.DataArray
        start_time: Start time string (e.g., '2000-01-01')
        end_time: End time string (e.g., '2000-12-31')
        
    Returns:
        Sliced dataset or data array
    """
    return data.sel(time=slice(start_time, end_time))


def extract_region(data, lat_range=None, lon_range=None):
    """
    Extract a spatial region from a dataset or data array.
    
    Args:
        data: xarray.Dataset or xarray.DataArray
        lat_range: Tuple of (min_lat, max_lat)
        lon_range: Tuple of (min_lon, max_lon)
        
    Returns:
        Region-extracted dataset or data array
    """
    result = data
    
    if lat_range is not None:
        if 'lat' in data.dims:
            result = result.sel(lat=slice(lat_range[0], lat_range[1]))
        elif 'latitude' in data.dims:
            result = result.sel(latitude=slice(lat_range[0], lat_range[1]))
    
    if lon_range is not None:
        if 'lon' in data.dims:
            result = result.sel(lon=slice(lon_range[0], lon_range[1]))
        elif 'longitude' in data.dims:
            result = result.sel(longitude=slice(lon_range[0], lon_range[1]))
    
    return result


def mask_land_ocean(data, mask_value, land=True):
    """
    Apply a land or ocean mask to data.
    
    Args:
        data: xarray.Dataset or xarray.DataArray
        mask_value: Value to use for masking
        land: If True, mask land; if False, mask ocean
        
    Returns:
        Masked dataset or data array
    """
    if isinstance(data, xr.Dataset):
        # Apply mask to all variables
        result = data.copy()
        for var in result.data_vars:
            result[var] = result[var].where(mask_value != 1 if land else mask_value == 1)
        return result
    else:
        # Apply mask to data array
        return data.where(mask_value != 1 if land else mask_value == 1)


def annual_cycle_climatology(data):
    """
    Calculate the annual cycle climatology.
    
    Similar to cdutil.ANNUALCYCLE.climatology().
    
    Args:
        data: xarray.DataArray with time dimension
        
    Returns:
        xarray.DataArray with monthly climatology
    """
    # Ensure we have an xcdat object for easy temporal operations
    if not hasattr(data, 'temporal'):
        data = xcdat.Dataset({"var": data}).var
    
    return data.temporal.climatology(freq="month")