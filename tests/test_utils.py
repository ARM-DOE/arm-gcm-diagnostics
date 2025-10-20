#!/usr/bin/env python
"""
Unit test for utils.py, verifying the xarray implementation works correctly.
"""

import unittest
import os
import sys
import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime

# Add the parent directory to the path so we can import arm_diags
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arm_diags.src.utils import climo, get_diurnal_cycle_seasons


class TestUtils(unittest.TestCase):
    """Test the utils.py module's xarray-based implementations."""

    def test_climo_monthly(self):
        """Test climo function with monthly data."""
        # Create a simple monthly dataset covering one year
        times = pd.date_range('2020-01-01', periods=12, freq='MS')
        data = np.arange(12) + 10  # Some sample data
        
        # Create xarray DataArray
        da = xr.DataArray(
            data=data,
            dims=["time"],
            coords={"time": times},
            name="test_var"
        )
        
        # Test with ANNUALCYCLE
        result = climo(da, 'ANNUALCYCLE')
        
        # Check result shape
        self.assertEqual(result.shape, (12,))
        
        # Check that values are as expected
        np.testing.assert_allclose(result, data)
        
        # Test with specific season
        result_jja = climo(da, 'JJA')
        expected_jja = np.mean(data[5:8])  # June, July, August
        self.assertAlmostEqual(result_jja[0], expected_jja)
    
    def test_climo_unit_conversion(self):
        """Test climo function with unit conversion."""
        # Create a simple monthly dataset covering one year
        times = pd.date_range('2020-01-01', periods=12, freq='MS')
        data = np.ones(12) * 300  # Temperature in Kelvin
        
        # Create xarray DataArray
        da = xr.DataArray(
            data=data,
            dims=["time"],
            coords={"time": times},
            name="tas"  # Temperature name triggers Kelvin to Celsius conversion
        )
        
        # Test with ANN
        result = climo(da, 'ANN')
        
        # Check that Kelvin to Celsius conversion happened
        self.assertAlmostEqual(result[0], 300 - 273.15)

    def test_get_diurnal_cycle_seasons(self):
        """Test get_diurnal_cycle_seasons function."""
        # Create a simple hourly dataset covering one year
        hours_in_year = 365 * 24
        times = pd.date_range('2020-01-01', periods=hours_in_year, freq='H')
        data = np.sin(np.linspace(0, 2*np.pi*365, hours_in_year)) + np.tile(np.sin(np.linspace(0, 2*np.pi, 24)), 365)
        
        # Create xarray DataArray
        da = xr.DataArray(
            data=data,
            dims=["time"],
            coords={"time": times}
        )
        
        # Test with JJA season
        seasons = ['JJA']
        years = [2020]
        result = get_diurnal_cycle_seasons(da, seasons, years)
        
        # Check result shape
        self.assertEqual(result.shape, (1, 1, 365, 24))
        
        # Verify that JJA data is in the right place (days 0-89)
        self.assertTrue(np.any(~np.isnan(result[0, 0, 0:90, :])))
        
        # Verify that non-JJA data is NaN
        self.assertTrue(np.all(np.isnan(result[0, 0, 90:, :])))


if __name__ == '__main__':
    unittest.main()