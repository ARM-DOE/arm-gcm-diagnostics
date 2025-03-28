"""
Configuration file for ARM Diagnostics.

This file contains default configuration parameters for the ARM Diagnostics package.
Users can override these values using environment variables or the CLI interface.
"""
import os

#===========================================================================================================================
#---------------------------------------------------------------------------------------------------------------------------
# The controller file of the ARM-DIAGS basic input parameters
# For changing the json file that controlling the diagnostic set options, please refer to arm_driver.py
#---------------------------------------------------------------------------------------------------------------------------
#===========================================================================================================================
# User defined case id
case_id = os.environ.get('ARM_DIAGS_CASE_ID', 'arm_diags_output')

# User defined the ARM-Diags package path - set to current directory by default
armdiags_path = os.environ.get('ARM_DIAGS_PATH', os.path.dirname(os.path.abspath(__file__)))

#--------------------------------------------------------------------------
# Testing model dataset (User defined model)
# Specify name of the test model to find the files
test_data_set = os.environ.get('ARM_DIAGS_TEST_MODEL', 'testmodel')

# Specify the data starting/ending years in the testmodel file
# Default is 1979 - 2006 as in the CMIP file
test_start_year = int(os.environ.get('ARM_DIAGS_TEST_START_YEAR', 1979))
test_end_year = int(os.environ.get('ARM_DIAGS_TEST_END_YEAR', 2006))

#--------------------------------------------------------------------------
# Set input path, where the model, observational and cmip data are located.
base_path = os.environ.get('ARM_DIAGS_BASE_PATH', './data/')
test_data_path = os.environ.get('ARM_DIAGS_TEST_DATA_PATH', os.path.join(base_path, 'testmodel'))
obs_path = os.environ.get('ARM_DIAGS_OBS_PATH', os.path.join(base_path, 'observation'))
cmip_path = os.environ.get('ARM_DIAGS_CMIP_PATH', os.path.join(base_path, 'cmip6'))

#--------------------------------------------------------------------------
# Set output path, where the results will be saved
output_path = os.environ.get('ARM_DIAGS_OUTPUT_PATH', os.path.join('./output', case_id))

arm_filename = True
#===========================================================================================================================
