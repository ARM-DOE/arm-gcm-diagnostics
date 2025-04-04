"""
Test parameter file for Diurnal Cycle Land-Atmosphere Coupling diagnostics only.
"""

# User defined case id
case_id = 'test_diurnal_cycle_LAcoupling_xarray'

# Paths to data directories
base_path = '/Users/zhang40/Documents/ARM/data/arm_diags_data_v4.0/'
test_data_path = base_path + 'testmodel'  # Path to test model data
obs_path = base_path + 'observation'      # Path to observational data
cmip_path = base_path + 'cmip6'           # Path to CMIP data
output_path = base_path + 'results/' + case_id  # Path where results will be saved

# Model information
test_data_set = 'testmodel'  # Name of the test model dataset

# Configuration file with only set11_diurnal_cycle_LAcoupling diagnostics
config_file = 'diags_set11_diurnal_cycle_LAcoupling.json'

# Additional options
arm_filename = True  # Whether to use ARM filename conventions

# Define reference models
ref_models = ['CanESM2', 'CMCC-CM', 'GFDL-CM3', 'GISS-E2-H', 'HadGEM2-A', 'NorESM1-M']

# Variables to analyze
variables = ['SH', 'LH', 'T_srf', 'RH_srf', 'LCL', 'pbl']
varnames = ['Surface Sensible Heat Flux', 'Surface Latent Heat Flux', 'Surface Temperature', 'Surface Relative Humidity', 'Lifting Condensation Level', 'Planetary Boundary Layer Height']
units = ['W/m$^2$', 'W/m$^2$', 'K', '%', 'm', 'm']

# Seasons to analyze
season = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']

# Sites to analyze
sites = ['sgpc1']  # Southern Great Plains