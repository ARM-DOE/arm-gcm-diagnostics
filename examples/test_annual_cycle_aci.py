"""
Test parameter file for Annual Cycle ACI diagnostics only.
"""

# User defined case id
case_id = 'test_annual_cycle_aci_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip6'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset

# Configuration file with only annual_cycle_aci diagnostics
config_file = 'diags_set8_cmip6.json'  # This contains only annual_cycle_aci diagnostics

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Define reference models
ref_models = ['CanESM2', 'CMCC-CM', 'GFDL-CM3', 'GISS-E2-H', 'HadGEM2-A', 'NorESM1-M']

# Month names for the annual cycle
season = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

# Variables to analyze (ACI-specific variables)
variables = ['ccn1', 'ccn2', 'cod', 'cod_liq', 'lwp', 'iwp', 'cpc', 'aod', 'so4_srf']

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains
