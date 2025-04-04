"""
Test parameter file for Convection Onset diagnostics only.
"""

# User defined case id
case_id = 'test_convection_onset_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip5'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset

# Configuration file with only convection_onset diagnostics
config_file = 'test_convection_onset_cmip5.json'  # This contains only set7_convection_onset diagnostics

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Define reference models
ref_models = ['CanESM2', 'CMCC-CM', 'GFDL-CM3', 'GISS-E2-H', 'HadGEM2-A', 'NorESM1-M']

# Variables to analyze (precipitation and column water vapor)
variables = ['pr', 'prw']

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains