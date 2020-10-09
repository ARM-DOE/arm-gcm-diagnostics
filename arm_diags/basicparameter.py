#test_data_set = 'cmip5cnrmcm5'        # Specify name of the test model to find the files
test_data_set = 'testmodel'
#test_data_set = 'cmip5cesm1cam5'
#test_data_set = 'cmip5gisse2r'
case_id = 'output_results_newname'

# Set input path, where the model, observational and cmip data are located.
base_path = '/Users/zhang40/Documents/ARM_LLNL/repo/ARMDiag_v2_data_20201007/'

#test_data_path = base_path+'cmip5'
test_data_path = base_path+'testmodel'
obs_path = base_path+'observation'
cmip_path =  base_path+'cmip5'

# Set output path, where the results will be saved
output_path = '/Users/zhang40/Documents/ARM_LLNL/repo/results/'+case_id

arm_filename = True
