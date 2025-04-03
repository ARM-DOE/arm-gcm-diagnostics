"""
Test parameter file for Annual Cycle diagnostics only.
"""

# User defined case id
case_id = 'test_annual_cycle_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip6'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset
test_start_year = 1979       # Start year for test data
test_end_year = 2006         # End year for test data

# Configuration file with only annual_cycle diagnostics
config_file = 'diags_set2_cmip5.json'  # This contains only set2_annual_cycle diagnostics

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Define reference models
ref_models = ['CanESM2', 'CMCC-CM', 'GFDL-CM3', 'GISS-E2-H', 'HadGEM2-A', 'NorESM1-M']

# Season for annual cycle
season = ['J','F','M','A','M','J','J','A','S','O','N','D']  # Months for annual cycle

# Variables to analyze
variables = ['tas', 'pr', 'clt']  # Temperature, precipitation, cloud fraction

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains