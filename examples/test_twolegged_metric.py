"""
Test parameter file for Two-Legged Metric (Land-Atmosphere Coupling) diagnostics only.
"""

# User defined case id
case_id = 'test_twolegged_metric_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip6'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset

# Configuration file containing only the Land-Atmosphere coupling diagnostics
config_file = 'diags_set10_twolegged_metrics_cmip6.json'

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains

# Seasons to analyze
season = ['MAM', 'JJA', 'SON', 'DJF']
