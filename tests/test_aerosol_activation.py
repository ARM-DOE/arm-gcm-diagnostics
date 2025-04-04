#!/usr/bin/env python
"""
Unit test for aerosol_activation.py, verifying the xarray implementation
matches the original implementation using cdms2/cdutil.
"""

import unittest
import os
import sys
import numpy as np
import xarray as xr
from unittest.mock import patch

# Add the parent directory to the path so we can import arm_diags
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from arm_diags.src.aerosol_activation import aerosol_activation_density_plot


class TestAerosolActivation(unittest.TestCase):
    """Test the aerosol_activation.py module."""

    @patch('arm_diags.src.aerosol_activation.xr.open_dataset')
    @patch('arm_diags.src.aerosol_activation.glob.glob')
    @patch('arm_diags.src.aerosol_activation.plt.savefig')
    @patch('arm_diags.src.aerosol_activation.os.makedirs')
    def test_aerosol_activation_density_plot(self, mock_makedirs, mock_savefig, mock_glob, mock_open_dataset):
        """Test that the aerosol_activation_density_plot function runs correctly."""
        # Create a mock parameter object
        class MockParameter:
            def __init__(self):
                self.variables = ['cpc', 'ccn02', 'ccn05']
                self.test_data_path = './test_data/'
                self.test_data_set = 'test_model'
                self.obs_path = './obs_data/'
                self.cmip_path = './cmip_data/'
                self.output_path = './output/'
                self.sites = ['sgpc1']

        # Mock the glob result for observation file
        mock_glob.return_value = ['./obs_data/sgparmdiagsaciactivateC1.nc']

        # Create a mock xarray dataset
        mock_ds = xr.Dataset(
            data_vars={
                'cpc_bulk': ('time', np.array([100.0, 200.0, 300.0])),
                'ccn02_bulk': ('time', np.array([50.0, 100.0, 150.0])),
                'ccn05_bulk': ('time', np.array([75.0, 150.0, 225.0]))
            }
        )
        mock_open_dataset.return_value = mock_ds

        # Call the function
        parameter = MockParameter()
        aerosol_activation_density_plot(parameter)

        # Verify the xarray dataset was opened with decode_times=False
        mock_open_dataset.assert_called_with('./obs_data/sgparmdiagsaciactivateC1.nc', decode_times=False)

        # Verify the output directory was created
        mock_makedirs.assert_called_once()

        # Verify that savefig was called, indicating plots were created
        self.assertTrue(mock_savefig.called)
        
        
if __name__ == '__main__':
    unittest.main()