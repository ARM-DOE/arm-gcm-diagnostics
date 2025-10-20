"""
Test parameter file for Seasonal Mean diagnostics only.
"""

# User defined case id
case_id = 'test_seasonal_mean_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip5'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset

# Configuration file with only seasonal_mean diagnostics
config_file = 'diags_set1_cmip5.json'  # This contains only set1_tables diagnostics

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Define reference models
ref_models = ['CanESM2', 'CMCC-CM', 'GFDL-CM3', 'GISS-E2-H', 'HadGEM2-A', 'NorESM1-M']

# Seasons to analyze
season = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']  # All seasons

# Variables to analyze
variables = ['tas', 'pr']  # Temperature and precipitation

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains