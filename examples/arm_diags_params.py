"""
Parameter file for ARM Diagnostics.

This file can be used to configure ARM Diagnostics settings without having to 
specify command-line arguments. Users can customize this file according to 
their specific requirements.

Usage:
  ./run_arm_diags.py -p /path/to/this/file
"""

# User defined case id
case_id = 'arm_diags_example_run'

# Paths to data directories
base_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip6'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset
test_start_year = 1979       # Start year for test data
test_end_year = 2006         # End year for test data

# Configuration file with diagnostics settings
# Use the default config file in the config directory
config_file = 'diags_all_multisites_for_cmip6.json'  # Default configuration
#config_file = 'diags_all_multisites_for_LAcoupling.json'

# Additional options
arm_filename = True  # Whether to use ARM filename conventions
