#===========================================================================================================================
#---------------------------------------------------------------------------------------------------------------------------
# The controller file of the ARM-DIAGS basic input parameters
# For changing the json file that controlling the diagnostic set options, please refer to arm_driver.py
#---------------------------------------------------------------------------------------------------------------------------
#===========================================================================================================================
# User defined case id
#case_id = 'output_cheng_20230705_mdtfv3_cesm'
case_id = 'output_mdtfv3_gfdl_20240814'

# User defined the ARM-Diags package path
armdiags_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/arm-gcm-diagnostics/'

#--------------------------------------------------------------------------
# Testing model dataset (User defined model)
# Specify name of the test model to find the files
test_data_set = 'testmodel'
#specify the data starting/ending years in the testmodel file
#default is 1979 - 2006 as in the CMIP file
#NCAR: 2013, 2014
#GFDL: 1980, 2000
test_start_year = 1980
test_end_year   = 2000

#--------------------------------------------------------------------------
# Set input path, where the model, observational and cmip data are located.
#base_path = '/DATA/ARM-Diag/arm-gcm-diagnostics/arm_diags/'
#base_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/arm_diags_data_v3.1_07052023_mdtfv3_cesm/'
#base_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/arm_diags_data_v3.1_05192023/'
base_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/arm_diags_data_v3.1_06292023_mdtfv3_gfdl/'
#base_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/arm_diags_data_v3.1_06122023/'
test_data_path = base_path+'testmodel'
obs_path = base_path+'observation'
cmip_path =  base_path+'cmip6'

#--------------------------------------------------------------------------
# Set output path, where the results will be saved
#output_path = '/DATA/ARM-Diag/Results/'+case_id
output_path = '/Users/tao4/Documents/ARM_Infrastructure/ARM_DIAG/'+case_id

arm_filename = True
#===========================================================================================================================
