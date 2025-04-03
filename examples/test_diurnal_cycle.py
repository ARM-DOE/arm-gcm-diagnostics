"""
Test parameter file for Diurnal Cycle diagnostics only.
"""

# User defined case id
case_id = 'test_diurnal_cycle_xarray_fft'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip5'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset
#test_start_year = 1979       # Start year for test data
#test_end_year = 2006         # End year for test data

# Configuration file with only diurnal_cycle diagnostics
config_file = 'diags_set4_cmip5.json'  # This contains only set4_diurnal_cycle diagnostics

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Define reference models
ref_models = ['CanESM2', 'CMCC-CM', 'GFDL-CM3', 'GISS-E2-H', 'HadGEM2-A', 'NorESM1-M']

# Season for diurnal cycle
season = ['JJA']  # Include all seasons

# Variables to analyze
variables = ['pr']  # Precipitation for diurnal cycle analysis

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains
