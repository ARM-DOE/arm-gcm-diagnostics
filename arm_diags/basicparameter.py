#test_data_set = 'cmip5cnrmcm5'        # name of the model, which should be included as the /model/test_data_xxxx.nc
test_data_set = 'testmodel'
case_id = 'output_results_newname_full'

# Set input path, where the model, observational and cmip data are located.
base_path = '/Users/zhang40/Documents/ARM_LLNL/repo/arm_diags_data_v2_release_fin_10072020/'

#test_data_path = base_path+'cmip5'
test_data_path = base_path+'testmodel'
obs_path = base_path+'observation'
cmip_path =  base_path+'cmip5'

# Set output path, where the results will be saved
output_path = '/Users/zhang40/Documents/ARM_LLNL/repo/results/'+case_id

arm_filename = True
