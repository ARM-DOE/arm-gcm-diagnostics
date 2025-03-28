"""
ARM Diagnostics Dataset Module.

This module provides the Dataset class for handling data operations
in the ARM Diagnostics package, similar to E3SM Diagnostics approach.
"""

import os
import numpy as np
import xarray as xr
import xcdat
import pandas as pd
import warnings

class Dataset:
    """
    Dataset class for ARM Diagnostics.
    
    This class handles dataset operations including loading, variable access,
    and time series extraction. It provides a consistent interface for working
    with model, observational, and reference datasets.
    """
    
    def __init__(self, filename, name=""):
        """
        Initialize a dataset from a netCDF file.
        
        Args:
            filename: Path to netCDF file
            name: Optional name for the dataset
        """
        self.filename = filename
        self.name = name or os.path.basename(filename)
        
        # Open dataset with xarray
        try:
            # Try using xcdat's open_dataset for better CF compliance
            self.ds = xcdat.open_dataset(filename)
        except:
            # Fall back to standard xarray
            self.ds = xr.open_dataset(filename)
    
    def get_variable(self, var_name, selector=None):
        """
        Get a variable from the dataset.
        
        Args:
            var_name: Variable name
            selector: Optional dictionary of coordinates for selection
            
        Returns:
            xarray.DataArray of the requested variable
        """
        # Find variable (case-insensitive)
        var_key = None
        for var in self.ds.variables:
            if var.lower() == var_name.lower():
                var_key = var
                break
        
        # Try standard_name if not found by name
        if var_key is None:
            for var in self.ds.variables:
                if hasattr(self.ds[var], 'standard_name') and self.ds[var].standard_name == var_name:
                    var_key = var
                    break
                    
        if var_key is None:
            raise ValueError(f"Variable {var_name} not found in dataset {self.name}")
            
        # Extract data
        da = self.ds[var_key]
        
        # Apply selector if provided
        if selector is not None:
            for key, value in selector.items():
                if key in da.coords:
                    da = da.sel({key: value})
        
        # Set variable ID for compatibility with cdms2-based code
        da.attrs['id'] = var_name
        
        return da
    
    def get_time_series_dataset(self, var_name, single_point=True, lat=None, lon=None):
        """
        Get time series dataset for a variable.
        
        This method extracts time series data for a variable, optionally at a specific point.
        
        Args:
            var_name: Variable name
            single_point: If True, extract data for a single point
            lat: Optional latitude value or range
            lon: Optional longitude value or range
            
        Returns:
            xarray.DataArray with time series data
        """
        # Get the variable as a DataArray
        da = self.get_variable(var_name)
        
        # Extract point data if requested
        if single_point and lat is not None and lon is not None:
            # Find the closest point to the requested coordinates
            if 'lat' in da.coords:
                da = da.sel(lat=lat, lon=lon, method='nearest')
            elif 'latitude' in da.coords:
                da = da.sel(latitude=lat, longitude=lon, method='nearest')
        
        return da
    
    def close(self):
        """Close the dataset."""
        self.ds.close()


def open_dataset(filename, name=""):
    """
    Open a dataset from a netCDF file.
    
    Args:
        filename: Path to netCDF file
        name: Optional name for the dataset
        
    Returns:
        Dataset object
    """
    return Dataset(filename, name)


def climatology(da, freq='monthly'):
    """
    Calculate climatology for a DataArray.
    
    Args:
        da: xarray.DataArray with time dimension
        freq: Frequency for climatology ('monthly', 'seasonal', 'annual')
        
    Returns:
        xarray.DataArray with climatology
    """
    # Ensure we have an xcdat.Dataset for temporal operations
    if not hasattr(da, 'temporal'):
        ds = xcdat.Dataset({'var': da})
        da = ds.var
    
    if freq == 'monthly':
        return da.temporal.climatology(freq='month')
    elif freq == 'seasonal':
        return da.temporal.climatology(freq='season')
    elif freq == 'annual':
        return da.temporal.climatology(freq='year')
    else:
        raise ValueError(f"Unsupported frequency: {freq}")


def composite_diurnal_cycle(da, var_name, season=None):
    """
    Create a composite diurnal cycle.
    
    Args:
        da: xarray.DataArray with time dimension
        var_name: Variable name
        season: Optional season name for filtering ('DJF', 'MAM', 'JJA', 'SON')
        
    Returns:
        tuple: (diurnal_cycle, local_time) arrays
    """
    # Ensure we have an xcdat.Dataset for temporal operations
    if not hasattr(da, 'temporal'):
        ds = xcdat.Dataset({'var': da})
        da = ds.var
    
    # Filter by season if requested
    if season and season != 'ANN':
        # Use xcdat's season selection
        da = da.temporal.group_seasonal_data(season=season)
    
    # Group by hour of day
    hourly_data = da.groupby('time.hour').mean(dim='time')
    
    # Convert to numpy array
    diurnal_cycle = hourly_data.values
    local_time = hourly_data.hour.values
    
    return diurnal_cycle, local_time