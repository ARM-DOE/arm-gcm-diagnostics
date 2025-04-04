"""
Test parameter file for Aerosol Activation diagnostics only.
"""

# User defined case id
case_id = 'test_aerosol_activation_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip6'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset

# Configuration file with only convection_onset diagnostics
config_file = 'diags_all_multisites_v3_cmip6_aerosol_activation.json'  # This contains only aerosol_activation diagnostics

# Additional options
arm_filename = True  # Whether to use ARM filename conventions


# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains
