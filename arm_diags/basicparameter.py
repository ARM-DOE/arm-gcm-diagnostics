#===========================================================================================================================
#---------------------------------------------------------------------------------------------------------------------------
# The controller file of the ARM-DIAGS basic input parameters
# For changing the json file that controlling the diagnostic set options, please refer to arm_driver.py
#---------------------------------------------------------------------------------------------------------------------------
#===========================================================================================================================
# User defined case id
case_id = 'V3_TestCMIP6'

#--------------------------------------------------------------------------
# Testing model dataset (User defined model)
# Specify name of the test model to find the files
test_data_set = 'testmodel'
#specify the data starting/ending years in the testmodel file
#default is 1979 - 2006 as in the CMIP file
test_start_year = 1979 
test_end_year   = 2006

#--------------------------------------------------------------------------
# Set input path, where the model, observational and cmip data are located.
base_path = '/DATA/ARM-Diag/arm-gcm-diagnostics/arm_diags/'

test_data_path = base_path+'testmodel'
obs_path = base_path+'observation'
cmip_path =  base_path+'cmip6'

#--------------------------------------------------------------------------
# Set output path, where the results will be saved
output_path = '/DATA/ARM-Diag/Results/'+case_id

arm_filename = True
#===========================================================================================================================
