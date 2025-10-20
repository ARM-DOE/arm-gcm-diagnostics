#===========================================================================================================================
# Program for generate annual/seasonal cycle & 2D plot from monthly data
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov-Dec 2021
    # ### unify the data extraction and process code for all the ARM sites
    # ### change the input/output format to site-dependent
    # ### change the 2D plots from color-mesh to color-contour
    # ### change the default treatments when test model not found
    # ---------------------------------------------------------------------------------------
# V4 Development
    # ---------------------------------------------------------------------------------------
    # Refactored to use xarray instead of cdms2/cdutil
    # Maintained original functionality while modernizing the code
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================
import os
import glob
import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt
from .varid_dict import varid_longname
import xarray as xr

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_zt_data(parameter):
    """
    Calculate annual cycle climatology with height-time (zt) data.
    
    This function processes 3D data (month, hour, vertical level) for 
    cloud profiles and saves the data in CSV format for plotting.
    """
    print("Starting annual_cycle_zt_data function")
    import traceback
    try:
        variables = parameter.variables
        seasons = parameter.season
        test_path = parameter.test_data_path
        obs_path = parameter.obs_path
        cmip_path = parameter.cmip_path
        output_path = parameter.output_path
        sites = parameter.sites
       
        test_model = parameter.test_data_set 
        ref_models = parameter.ref_models
        arm_name = parameter.arm_filename

        print('============================================================')
        print(f'Create CF Vertical Profiles: {sites[0]}')
        print('============================================================')

        # Create output directory if it doesn't exist
        if not os.path.exists(os.path.join(output_path, 'metrics', sites[0])):
            os.makedirs(os.path.join(output_path, 'metrics', sites[0]))

        # Calculate for test model
        test_findex = 0  # preset of test model indicator
        month = seasons  # Month names for labeling in output files
        
        # Construct file pattern based on naming convention
        if not arm_name:
            test_file = glob.glob(os.path.join(test_path, f'*{test_model}*diurnal*{sites[0]}.nc'))
        else:
            test_model_clean = ''.join(e for e in test_model if e.isalnum()).lower()
            print(f"{test_path}, {test_model_clean}, {sites[0][:3]}{test_model_clean}diurnalclim{sites[0][3:5].upper()}")
            test_file = glob.glob(os.path.join(test_path, f"{sites[0][:3]}{test_model_clean}diurnalclim{sites[0][3:5].upper()}*.nc"))

        if len(test_file) == 0:
            print(f'No climatology data for test model were found: {sites[0]}')
        else:
            # Test model exists
            test_findex = 1
            
            # Open dataset with xarray, prevent time decoding issues
            test_ds = xr.open_dataset(test_file[0], decode_times=False)
            print(f'Processing climatology data for test_model: {test_model}')
            
            # Process each variable
            for j, variable in enumerate(variables): 
                try:
                    # Handle 'cl' and 'cl_p' variables that might be named differently
                    var_name = variable
                    if variable == 'cl' or variable == 'cl_p':
                        if 'cl_p' in test_ds:
                            var_name = 'cl_p'
                        elif 'cl' in test_ds:
                            var_name = 'cl'
                    
                    if var_name in test_ds:
                        # Extract the variable as a numpy array
                        var_data = test_ds[var_name].values
                        
                        # Filter out unrealistic values
                        var_data = np.where(var_data > 100, np.nan, var_data)
                        
                        # Get the data length and reshape
                        len_var = var_data.shape[0]
                        var_2d = np.reshape(var_data, (12, int(len_var/12.), 37))
                        
                        # Save to CSV with appropriate formatting
                        with open(f"{output_path}/metrics/{sites[0]}/{variable}_test_diurnal_climo_{sites[0]}.csv", 'w') as outfile:
                            outfile.write(f'# Array shape: {var_2d.shape} as (month, hours, vertical levels)\n')
                            for mon_id, data_slice in enumerate(var_2d):
                                outfile.write(f'#{month[mon_id]} slice\n')
                                np.savetxt(outfile, data_slice, fmt='%-7.2f')
                    else:
                        print(f"{variable} not found in test dataset")
                except Exception as e:
                    print(f"{variable} not processed for {test_model}: {e}")
                    traceback.print_exc()
            
            # Close the dataset
            test_ds.close()

        # Calculate for observational data
        # Construct file pattern based on naming convention
        if not arm_name:
            obs_file = glob.glob(os.path.join(obs_path, f'*ARMdiag_*_diurnal_climo_{sites[0]}*.nc'))
        else:
            obs_file = glob.glob(os.path.join(obs_path, f"{sites[0][:3]}armdiagsmondiurnalclim{sites[0][3:5].upper()}*c1.nc"))

        print(f'ARM data: {sites[0]}')
        
        if len(obs_file) == 0:
            print(f"No observational data found for {sites[0]}")
        else:
            # Open dataset with xarray, prevent time decoding issues
            obs_ds = xr.open_dataset(obs_file[0], decode_times=False)
            
            # Process each variable
            for j, variable in enumerate(variables): 
                try:
                    if variable in obs_ds:
                        # Extract the variable as a numpy array
                        var_data = obs_ds[variable].values
                        
                        # Filter out unrealistic values for cloud fraction
                        var_data = np.where(var_data > 100, np.nan, var_data)
                        
                        # Reshape to (months, hours, levels)
                        var_2d = np.reshape(var_data, (12, 24, 37))
                        
                        # Save to CSV with appropriate formatting
                        with open(f"{output_path}/metrics/{sites[0]}/{variable}_obs_diurnal_climo_{sites[0]}.csv", 'w') as outfile:
                            outfile.write(f'# Array shape: {var_2d.shape} as (month, hours, vertical levels)\n')
                            for mon_id, data_slice in enumerate(var_2d):
                                outfile.write(f'#{month[mon_id]} slice\n')
                                np.savetxt(outfile, data_slice, fmt='%-7.2f')
                    else:
                        print(f"{variable} not found in observation dataset")
                except Exception as e:
                    print(f"{variable} not processed for obs: {e}")
                    traceback.print_exc()
            
            # Close the dataset
            obs_ds.close()
    except Exception as e:
        print(f"Error in annual_cycle_zt_data: {e}")
        traceback.print_exc()
        raise
         
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_zt_plot(parameter):
    """
    Prepare annual cycle and diurnal cycle plots of cloud fraction.
    
    This function creates various visualization plots:
    1. Monthly mean diurnal cycle contour plots
    2. Diurnal cycle contour plots
    3. Annual cycle contour plots
    4. Seasonal and annual mean vertical profile plots
    """
    print("Starting annual_cycle_zt_plot function")
    import traceback
    try:
        variables = parameter.variables
        seasons = parameter.season
        output_path = parameter.output_path
        sites = parameter.sites

        # Create output directory if it doesn't exist
        figures_dir = os.path.join(output_path, 'figures', sites[0])
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)

        # Check if test model data exists
        test_findex = 0  # preset of test model indicator
        test_file = glob.glob(os.path.join(output_path, 'metrics', sites[0], f'cl_p_test_diurnal_climo_{sites[0]}.csv'))
        if not test_file:
            print(f'No test model plotted for cl_p: {sites[0]}')
        else:
            test_findex = 1  # test model exists

        month = seasons
        month_legend = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Process each variable
        for j, variable in enumerate(variables):
            # Process test model data if available
            if test_findex == 1:
                try:
                    test_data_file = os.path.join(output_path, 'metrics', sites[0], f'{variable}_test_diurnal_climo_{sites[0]}.csv')
                    test_data = np.loadtxt(test_data_file)
                    
                    # Auto-detect the test model time frequency
                    len_var = test_data.shape[0]
                    tlen_testVar = int(len_var/12.)  # e.g., 24 or 8
                    tlen_testGap = 24/tlen_testVar   # e.g., 1hr or 3hr

                    # Reshape to (months, hours, levels)
                    test_data = test_data.reshape((12, tlen_testVar, 37))

                    # Calculate means along different dimensions
                    cl_p = np.nanmean(test_data, axis=1)  # Monthly mean (hours averaged out)
                    cl_p_diurnal = np.nanmean(test_data, axis=0)  # Diurnal mean (months averaged out)
                    cl_p_ann = np.nanmean(cl_p, axis=0)  # Annual mean (all months and hours averaged out)
                except Exception as e:
                    print(f"Error processing test data for {variable}: {e}")
                    test_findex = 0  # Reset if test data can't be processed
        
            try:
                # Process observation data
                obs_data_file = os.path.join(output_path, 'metrics', sites[0], f'{variable}_obs_diurnal_climo_{sites[0]}.csv')
                obs_data = np.loadtxt(obs_data_file)
                obs_data = obs_data.reshape((12, 24, 37))  # Always 24 hours in obs data

                # Calculate means along different dimensions
                cl_ob = np.nanmean(obs_data, axis=1)  # Monthly mean (hours averaged out)
                cl_ob_diurnal = np.nanmean(obs_data, axis=0)  # Diurnal mean (months averaged out)
                cl_ob_ann = np.nanmean(cl_ob, axis=0)  # Annual mean (all months and hours averaged out)
            except Exception as e:
                print(f"Error processing observation data for {variable}: {e}")
                continue  # Skip this variable if obs data can't be processed

        #################### Monthly Mean Diurnal Cycle Contours ####################
        # Define site-dependent contour levels and local time offset
        site_config = {
            'sgpc1': {'ct_lo': 0, 'ct_up': 25.5, 'locoff': 6},
            'nsac1': {'ct_lo': 0, 'ct_up': 50.5, 'locoff': 8},
            'enac1': {'ct_lo': 0, 'ct_up': 35.5, 'locoff': 1},
            'twpc1': {'ct_lo': 0, 'ct_up': 70.5, 'locoff': 14},
            'twpc2': {'ct_lo': 0, 'ct_up': 70.5, 'locoff': 12},
            'twpc3': {'ct_lo': 0, 'ct_up': 60.5, 'locoff': 15},
            'maom1': {'ct_lo': 0, 'ct_up': 80.5, 'locoff': 4}
        }
        
        # Get site-specific configuration with defaults if site not in dictionary
        site_cfg = site_config.get(sites[0], {'ct_lo': 0, 'ct_up': 50.0, 'locoff': 6})
        ct_lo = site_cfg['ct_lo']
        ct_up = site_cfg['ct_up']
        locoff = site_cfg['locoff']
        
        # Adjust contour upper limit based on actual data
        if test_findex == 0:
            ct_up = np.nanmax(obs_data.flatten())
            index_list = np.arange(1)
        else:
            ct_up = np.nanmax(np.concatenate((obs_data.flatten(), test_data.flatten()), axis=0))
            index_list = np.arange(2)
        
        rlevel = np.arange(ct_lo, ct_up+1, 0.5)
        
        # Plot monthly mean diurnal cycle contours (observations and model if available)
        for iid, index in enumerate(index_list):
            # Create figure with 4x3 subplots
            fig1, axs = plt.subplots(4, 3, figsize=(15, 12), facecolor='w', edgecolor='k', sharex=True, sharey=True)
            fig1.subplots_adjust(hspace=0.3, wspace=0.1)
            axs = axs.ravel()
            
            # Create a subplot for each month
            for imon in range(12):
                if index == 0:  # Observation data
                    title = f'{variable}_mon_diurnal_clim_obs'
                    yy = np.linspace(0, 23, 24)
                    xx = np.linspace(100, 1000, 37)
                    x, y = np.meshgrid(xx, yy)
                    
                    # Concatenate data for wrapping around local time conversion
                    obs_data_con = np.concatenate((obs_data[imon, :, :], obs_data[imon, :, :]), axis=0)
                    
                    # Plot using contourf
                    im = axs[imon].contourf(y, x, obs_data_con[locoff:locoff+24, ::-1], 
                                           cmap='jet', levels=rlevel)
                    
                    plt.xlim([0, 23])
                    xax = np.arange(0, 24, 3)
                    my_xticks = ['0', '3', '6', '9', '12', '15', '18', '21']

                else:  # Test model data
                    title = f'{variable}_mon_diurnal_clim_mod'
                    yy = np.linspace(0, tlen_testVar-1, tlen_testVar)
                    xx = np.linspace(100, 1000, 37)
                    x, y = np.meshgrid(xx, yy)
                    
                    # Concatenate data for wrapping around local time conversion
                    test_data_con = np.concatenate((test_data[imon, :, :], test_data[imon, :, :]), axis=0)
                    
                    # Handle different time resolutions
                    if tlen_testGap == 3:  # 3-hourly data
                        test_pstart = round(locoff/tlen_testGap) - 1
                        if test_pstart < 0:
                            test_pstart = 0
                        im = axs[imon].contourf(y, x, test_data_con[test_pstart:test_pstart+8, ::-1], 
                                               cmap='jet', levels=rlevel)
                    else:  # 1-hourly data
                        im = axs[imon].contourf(y, x, test_data_con[locoff:locoff+24, ::-1], 
                                               cmap='jet', levels=rlevel)
                    
                    plt.xlim([0, tlen_testVar-1])
                    xax = np.arange(0, tlen_testVar, int(tlen_testVar/8))
                    my_xticks = ['0', '3', '6', '9', '12', '15', '18', '21']

                # Set title and ticks
                axs[imon].set_title(month_legend[imon], fontsize=17)
                plt.xticks(xax, my_xticks)
                plt.setp(axs[imon].get_xticklabels(), visible=True)
            
            # Set labels for the bottom row
            for ax in axs[9:12]:
                ax.set_xlabel('Local time (hr)', fontsize=17)
            
            # Set labels for the left column
            for ax in axs[::3]:
                ax.set_ylabel('Pressure (mb)', fontsize=17)
            
            # Invert y-axis to have pressure decrease upward
            axs[0].invert_yaxis()
            
            # Set title and colorbar
            plt.suptitle(title, fontsize=30)
            fig1.subplots_adjust(right=0.8)
            cbar_ax = fig1.add_axes([0.85, 0.15, 0.05, 0.7])
            cb = fig1.colorbar(im, cax=cbar_ax)
            cb.ax.tick_params(labelsize=15)
            plt.title('cl (%)', fontsize=15)
            
            # Save figure and clean up
            fig_path = os.path.join(output_path, 'figures', sites[0], f'{title}_{sites[0]}.png')
            fig1.savefig(fig_path)
            plt.close('all')

        ########################## Diurnal Cycle Contours ####################
        # Update contour levels for diurnal cycle plots
        site_cfg = site_config.get(sites[0], {'ct_lo': 0, 'ct_up': 50.0, 'locoff': 6})
        ct_lo = site_cfg['ct_lo']
        locoff = site_cfg['locoff']
        
        # Different upper limit for diurnal cycle
        if sites[0] == 'nsac1': ct_up = 30.5
        if sites[0] == 'twpc2': ct_up = 40.5
        if sites[0] == 'twpc3': ct_up = 40.5
        
        # Adjust contour upper limit based on actual data
        if test_findex == 0:
            ct_up = np.nanmax(cl_ob_diurnal.flatten())
        else:
            ct_up = np.nanmax(np.concatenate((cl_ob_diurnal.flatten(), cl_p_diurnal.flatten()), axis=0))
        
        rlevel = np.arange(ct_lo, ct_up+1, 0.5)
        
        # Plot diurnal cycle contours (observations and model if available)
        for iid, index in enumerate(index_list):
            fig2 = plt.figure()
            ax = fig2.add_axes([0.15, 0.15, 0.65, 0.75])
            
            if index == 0:  # Observation data
                title = f'{variable}_diurnal_clim_obs'
                yy = np.linspace(0, 23, 24)
                xx = np.linspace(100, 1000, 37)
                x, y = np.meshgrid(xx, yy)
                
                # Concatenate data for wrapping around local time conversion
                obs_data_con = np.concatenate((cl_ob_diurnal, cl_ob_diurnal), axis=0)
                
                # Plot using contourf
                im = ax.contourf(y, x, obs_data_con[locoff:locoff+24, ::-1], 
                                cmap='jet', levels=rlevel)
                
                plt.xlim([0, 23])
                xax = np.arange(0, 24, 3)
                my_xticks = ['0', '3', '6', '9', '12', '15', '18', '21']

            else:  # Test model data
                title = f'{variable}_diurnal_clim_mod'
                yy = np.linspace(0, tlen_testVar-1, tlen_testVar)
                xx = np.linspace(100, 1000, 37)
                x, y = np.meshgrid(xx, yy)
                
                # Concatenate data for wrapping around local time conversion
                test_data_con = np.concatenate((cl_p_diurnal, cl_p_diurnal), axis=0)
                
                # Handle different time resolutions
                if tlen_testGap == 3:  # 3-hourly data
                    test_pstart = round(locoff/tlen_testGap) - 1
                    if test_pstart < 0:
                        test_pstart = 0
                    im = ax.contourf(y, x, test_data_con[test_pstart:test_pstart+8, ::-1], 
                                    cmap='jet', levels=rlevel)
                else:  # 1-hourly data
                    im = ax.contourf(y, x, test_data_con[locoff:locoff+24, ::-1], 
                                    cmap='jet', levels=rlevel)
                
                plt.xlim([0, tlen_testVar-1])
                xax = np.arange(0, tlen_testVar, int(tlen_testVar/8))
                my_xticks = ['0', '3', '6', '9', '12', '15', '18', '21']

            # Set labels and ticks
            plt.xticks(xax, my_xticks)
            plt.ylabel('Pressure (mb)')
            plt.xlabel('Local time (hr)')
            plt.gca().invert_yaxis()
            plt.suptitle(title)
            
            # Add colorbar
            cbar_ax = fig2.add_axes([0.85, 0.15, 0.05, 0.75])
            cb = fig2.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            
            # Save figure and clean up
            fig_path = os.path.join(output_path, 'figures', sites[0], f'{title}_{sites[0]}.png')
            fig2.savefig(fig_path)
            plt.close('all')

        ########################## Annual Cycle Contours ####################
        # Define plotting controller
        if test_findex == 0:
            aindex_list = np.arange(1)  # Only observation
        else:
            aindex_list = np.arange(3)  # Observation, model, and difference

        # Create meshgrid for annual cycle
        yy = np.linspace(0, 11, 12)
        xx = np.linspace(100, 1000, 37)
        x, y = np.meshgrid(xx, yy)
        
        # Define site-dependent contour levels for annual cycle and difference
        annual_site_config = {
            'sgpc1': {'ct_lo': 0, 'ct_up': 25.5, 'ct_lo_diff': -10, 'ct_up_diff': 10.5},
            'nsac1': {'ct_lo': 0, 'ct_up': 60.5, 'ct_lo_diff': -35, 'ct_up_diff': 40.5},
            'enac1': {'ct_lo': 0, 'ct_up': 35.5, 'ct_lo_diff': -15, 'ct_up_diff': 20.5},
            'twpc1': {'ct_lo': 0, 'ct_up': 70.5, 'ct_lo_diff': -10, 'ct_up_diff': 40.5},
            'twpc2': {'ct_lo': 0, 'ct_up': 60.5, 'ct_lo_diff': -10, 'ct_up_diff': 50.5},
            'twpc3': {'ct_lo': 0, 'ct_up': 40.5, 'ct_lo_diff': -20, 'ct_up_diff': 15.5},
            'maom1': {'ct_lo': 0, 'ct_up': 70.5, 'ct_lo_diff': -15, 'ct_up_diff': 60.5}
        }
        
        # Get site-specific configuration with defaults if site not in dictionary
        annual_cfg = annual_site_config.get(sites[0], 
                                           {'ct_lo': 0, 'ct_up': 50.0, 
                                            'ct_lo_diff': -20, 'ct_up_diff': 20.0})
        ct_lo = annual_cfg['ct_lo']
        ct_up = annual_cfg['ct_up']
        ct_lo_diff = annual_cfg['ct_lo_diff']
        ct_up_diff = annual_cfg['ct_up_diff']
        
        # Adjust contour limits based on actual data
        if test_findex == 0:
            ct_up = np.nanmax(cl_ob)
        else:
            ct_up = np.nanmax([cl_ob, cl_p])
            tmpct = cl_p[:, ::-1] - cl_ob[:, ::-1]
            ct_lo_diff = int(np.nanmin(tmpct) - 1)
            ct_up_diff = int(np.nanmax(tmpct) + 1)

        # Create contour levels
        rlevel = np.arange(ct_lo, ct_up+1, 0.5)
        drlevel = np.arange(ct_lo_diff, ct_up_diff, 0.5)
        
        # Plot annual cycle contours
        for iid, index in enumerate(aindex_list):
            fig = plt.figure()
            ax = fig.add_axes([0.15, 0.15, 0.65, 0.75])
            
            if index == 0:  # Observation
                im = ax.contourf(y, x, cl_ob[:, ::-1], cmap='jet', levels=rlevel)
                title = f'{variable}_annual_cycle_clim_obs_{sites[0]}'
            elif index == 1:  # Test model
                im = ax.contourf(y, x, cl_p[:, ::-1], cmap='jet', levels=rlevel)
                title = f'{variable}_annual_cycle_clim_mod_{sites[0]}'
            elif index == 2:  # Difference
                im = ax.contourf(y, x, cl_p[:, ::-1]-cl_ob[:, ::-1], cmap='coolwarm', levels=drlevel)
                title = f'{variable}_annual_cycle_clim_the_diff_{sites[0]}'
            
            # Set x-axis labels to month abbreviations
            xax = np.arange(0, 12, 1)
            my_xticks = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
            plt.xticks(xax, my_xticks)
            plt.xlim(0, 11)
            
            # Set labels and invert y-axis
            plt.ylabel('Pressure (mb)')
            plt.xlabel('Month')
            plt.gca().invert_yaxis()
            plt.suptitle(title)
            
            # Add colorbar
            cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.75])
            cb = fig.colorbar(im, cax=cbar_ax)
            plt.title('cl (%)')
            
            # Save figure and clean up
            fig_path = os.path.join(output_path, 'figures', sites[0], f'{title}.png')
            fig.savefig(fig_path)
            plt.close('all')

        ########################### Seasonal Mean Vertical Profile Plots ####################
        levels = xx
        seasons = ['MAM', 'JJA', 'SON', 'DJF']
        
        # Concatenate data for seasonal calculations
        if test_findex == 1:
            cl_p2 = np.concatenate((cl_p, cl_p), axis=0)
        cl_ob2 = np.concatenate((cl_ob, cl_ob), axis=0)
        
        # Determine x-axis upper limit
        if test_findex == 0:
            xtup = np.nanmax(cl_ob2.flatten())
        else:
            xtup = np.nanmax(np.concatenate((cl_ob2.flatten(), cl_p2.flatten()), axis=0))
        
        # Plot seasonal mean vertical profiles
        for index in range(len(seasons)):
            fig3 = plt.figure(figsize=(10, 15))
            ax = fig3.add_axes([0.15, 0.07, 0.80, 0.88])
            
            # Plot model data if available
            if test_findex == 1:
                ax.plot(np.nanmean(cl_p2[index*3+2:(index+1)*3+2, ::-1], axis=0), 
                        levels, 'r', lw=3, label='MOD')
            
            # Plot observation data
            ax.plot(np.nanmean(cl_ob2[index*3+2:(index+1)*3+2, ::-1], axis=0), 
                    levels, 'k', lw=3, label='OBS')
            
            # Set labels, limits, and other formatting
            plt.gca().invert_yaxis()
            plt.ylabel('Pressure (mb)', fontsize=20)
            plt.xlabel('Cloud Fraction (%)', fontsize=20)
            plt.xlim([0, xtup])
            plt.legend(loc='best', prop={'size': 25})
            ax.tick_params(labelsize=20, length=5, width=1, direction='out', which='major')
            plt.title(f'{seasons[index]} Mean Cloud Fraction Vertical Profile', fontsize=20)
            
            # Save figure and clean up
            fig_path = os.path.join(output_path, 'figures', sites[0], 
                                   f'{variable}_zdiff_{seasons[index]}_{sites[0]}.png')
            fig3.savefig(fig_path)
            plt.close('all')

        ########################### Annual Mean Vertical Profile Plot ####################
        fig0 = plt.figure(figsize=(10, 15))
        ax = fig0.add_axes([0.15, 0.07, 0.80, 0.88])
        
        # Plot model data if available
        if test_findex == 1:
            ax.plot(cl_p_ann[::-1], levels, 'r', lw=3, label='MOD')
        
        # Plot observation data
        ax.plot(cl_ob_ann[::-1], levels, 'k', lw=3, label='OBS')
        
        # Set labels, limits, and other formatting
        plt.gca().invert_yaxis()
        plt.ylabel('Pressure (mb)', fontsize=20)
        plt.xlabel('Cloud Fraction (%)', fontsize=20)
        plt.xlim([0, xtup])
        plt.legend(loc='best', prop={'size': 25})
        ax.tick_params(labelsize=20, length=5, width=1, direction='out', which='major')
        plt.title('Annual Mean Cloud Fraction Vertical Profile', fontsize=20)
        
        # Save figure and clean up
        fig_path = os.path.join(output_path, 'figures', sites[0], 
                               f'{variable}_zdiff_ANN_{sites[0]}.png')
        fig0.savefig(fig_path)
        plt.close('all')
    except Exception as e:
        print(f"Error in annual_cycle_zt_plot: {e}")
        traceback.print_exc()
        raise
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

