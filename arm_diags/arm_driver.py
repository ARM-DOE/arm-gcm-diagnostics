#!/usr/bin/env python
import json
import copy
import numpy
import shutil
import glob
import os
import pdb
import fnmatch
import pathlib

# Handle Python version differences for importlib.resources
try:
    # For Python 3.10+
    from importlib.resources import files
except ImportError:
    # For Python 3.9
    from importlib_resources import files

from .src.seasonal_mean import seasonal_mean_table
from .src.annual_cycle import annual_cycle_data, annual_cycle_line_plot, annual_cycle_taylor_diagram
from .src.annual_cycle_aci import annual_cycle_aci_data, annual_cycle_aci_line_plot, annual_cycle_aci_taylor_diagram
from .src.annual_cycle_zt import annual_cycle_zt_data, annual_cycle_zt_plot
from .src.diurnal_cycle import diurnal_cycle_data, diurnal_cycle_plot
from .src.pdf_daily import pdf_daily_data, pdf_daily_plot
from .src.convection_onset_driver import convection_onset
from .src.aerosol_activation import aerosol_activation_density_plot
from .src.twolegged_metric import twolegged_metric_plot
from .src.diurnal_cycle_LAcoupling import diurnal_cycle_LAcoupling_plot

from .src.create_htmls import (
    annual_cycle_zt_html,
    diurnal_cycle_zt_html,
    diurnal_cycle_html,
    seasonal_mean_table_html,
    annual_cycle_html,
    annual_cycle_aci_html,
    pdf_daily_html,
    convection_onset_html,
    aerosol_activation_html,
    twolegged_metric_html,
    diurnal_cycle_LAcoupling_html,
    diags_main_html
)
def make_parameters(basic_parameter):
    """Create parameter objects from a JSON configuration file.
    
    Parameters
    ----------
    basic_parameter : object
        Object containing basic parameters, including config_file if specified
        
    Returns
    -------
    list
        List of parameter objects for each diagnostic set
    """
    # Get config file name from parameter object or use default
    config_file = getattr(basic_parameter, 'config_file', 'diags_all_multisites_for_cmip6.json')
    
    # Try to locate the config file, checking multiple locations
    config_path = config_file  # First assume it's a direct path provided by user
    
    # If not a direct path, try various locations
    if not os.path.isfile(config_path):
        # Try in package config directory first (default configs are here)
        config_dir_path = files('arm_diags') / 'config' / config_file
        if config_dir_path.exists():
            config_path = config_dir_path
        else:
            # Try in examples directory next
            example_path = files('arm_diags') / 'examples' / config_file
            if example_path.exists():
                config_path = example_path
    
    # Read and parse the JSON file
    try:
        with open(config_path, 'r') as f:
            f_data = f.read()
    except FileNotFoundError:
        # Provide a more helpful error message
        searched_paths = [
            f"Current directory: {os.path.abspath(config_file)}",
            f"Package config directory: {files('arm_diags') / 'config' / config_file}",
            f"Package examples directory: {files('arm_diags') / 'examples' / config_file}"
        ]
        error_msg = (
            f"Could not find configuration file: {config_file}\n\n"
            f"Searched in the following locations:\n" + 
            "\n".join(f"- {path}" for path in searched_paths) +
            "\n\nPlease provide a valid path to a configuration file."
        )
        raise FileNotFoundError(error_msg)
        
    json_file = json.loads(f_data)

    parameters = [] 
    for key in json_file:
        print((json_file[key],key))
        for single_run in json_file[key]:
            p = copy.deepcopy(basic_parameter)
            for attr_name in single_run:
                setattr(p, attr_name, single_run[attr_name])
            parameters.append(p)
    return parameters

# Read in specification files, including those from:
# 1. basicparameter.py
# 2. diags_sets.json

# Only run this section if this file is being executed directly (not imported)
if __name__ == "__main__":
    # Import arm_parser here (requires cdp package from conda-forge)
    try:
        from . import arm_parser
    except ImportError:
        print("Warning: Could not import arm_parser. This requires the 'cdp' package from conda-forge.")
        print("Install it with: conda install -c conda-forge cdp")
        print("For running diagnostics, use run_arm_diags.py instead, which doesn't require cdp.")
        raise

    parser = arm_parser.ARMParser()
    basic_parameter = parser.get_orig_parameters(argparse_vals_only=False)
    #basic_parameter = parser.get_parameters()
    parameters = make_parameters(basic_parameter)
    
    case_id = basic_parameter.case_id
    output_path = basic_parameter.output_path
    test_model = basic_parameter.test_data_set
    print('output_path: ', output_path)

    # Generate new case folder given case_id:
    if not os.path.exists(os.path.join(output_path)):
        os.makedirs(output_path)
        os.makedirs(os.path.join(output_path,'html'))
        os.makedirs(os.path.join(output_path,'figures'))
        os.makedirs(os.path.join(output_path,'metrics'))
    
    # Copy the logo figures to the newly created html folder using importlib.resources
    misc_dir = files('arm_diags') / 'misc'
    dst = os.path.join(output_path, 'html')
    for src_file in misc_dir.iterdir():
        if src_file.is_file():
            shutil.copy(src_file, dst)
    
    # Loop through diagnostic sets prespecified from diags_sets.json
    html_count = 0
    for parameter in parameters:
        diags_set = parameter.diags_set
        output_path = parameter.output_path
        test_model = parameter.test_data_set
        
        # set1 diagnostics
        if diags_set == 'set1_tables':
            try:
                seasonal_mean_table(parameter) #Calculate seasonal mean climatology
                seasonal_mean_table_html(parameter) #Generate html 
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set2_annual_cycle':
            try:
                annual_cycle_data(parameter)
                annual_cycle_line_plot(parameter)
                annual_cycle_taylor_diagram(parameter)
                annual_cycle_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set3_annual_cycle_zt': # this also include set5 diags
            try:
                annual_cycle_zt_data(parameter)
                annual_cycle_zt_plot(parameter)
                annual_cycle_zt_html(parameter)
                diurnal_cycle_zt_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set4_diurnal_cycle':
            try:
                diurnal_cycle_data(parameter)
                diurnal_cycle_plot(parameter)
                diurnal_cycle_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set6_pdf_daily':
            try:
                pdf_daily_data(parameter)
                pdf_daily_plot(parameter)
                pdf_daily_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set7_convection_onset':
            try:
                convection_onset(parameter)
                convection_onset_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set8_annual_cycle_aci':
            try:
                annual_cycle_aci_data(parameter)
                annual_cycle_aci_line_plot(parameter)
                annual_cycle_aci_taylor_diagram(parameter)
                annual_cycle_aci_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set9_aerosol_activation':
            try:
                aerosol_activation_density_plot(parameter)
                aerosol_activation_html(parameter)
                html_count = html_count + 1
            except:
                pass
         
        if diags_set == 'set10_twolegged_metric':
            try:
                twolegged_metric_plot(parameter)
                twolegged_metric_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set11_diurnal_cycle_LAcoupling':
            try:
                diurnal_cycle_LAcoupling_plot(parameter)
                diurnal_cycle_LAcoupling_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
    # Create the main html page hosting all sets of diagnostics
    if html_count >= 1:
        diags_main_html(output_path, test_model)
        #
        print(('Html files saved in:'+output_path+'/html/'))
        print(('Open Html file by (MacOS): open ' +output_path+'/html/arm_diag.html'))
        print(('Open Html file by (Linux): xdg-open ' +output_path+'/html/arm_diag.html'))
        
        print('Processes Completed!')
        print('------------------     END    -------------------------')
    else:
        print('Unable to process data. No diagnostic set was run and no html was generated!')


def run_diagnostics(basic_parameter):
    """Run ARM diagnostics with the given parameters.
    
    This function serves as the main entry point for running the diagnostics
    when called from external scripts.
    
    Parameters
    ----------
    basic_parameter : object
        Object containing all necessary parameters for the diagnostics
    """
    # Make a copy of basic_parameter to avoid modifying the original
    basic_parameter_copy = copy.deepcopy(basic_parameter)
    
    # Process parameter file to create set of parameters for each diagnostic
    parameters = make_parameters(basic_parameter_copy)
    
    # Get key parameters
    case_id = basic_parameter.case_id
    output_path = basic_parameter.output_path
    test_model = basic_parameter.test_data_set
    print('output_path: ', output_path)
    
    # Generate new case folder given case_id:
    if not os.path.exists(os.path.join(output_path)):
        os.makedirs(output_path)
        os.makedirs(os.path.join(output_path, 'html'))
        os.makedirs(os.path.join(output_path, 'figures'))
        os.makedirs(os.path.join(output_path, 'metrics'))
    
    # Copy the logo figures to the newly created html folder using importlib.resources
    misc_dir = files('arm_diags') / 'misc'
    dst = os.path.join(output_path, 'html')
    for src_file in misc_dir.iterdir():
        if src_file.is_file():
            shutil.copy(src_file, dst)
    
    # Loop through diagnostic sets prespecified from diags_sets.json
    html_count = 0
    for parameter in parameters:
        diags_set = parameter.diags_set
        output_path = parameter.output_path
        test_model = parameter.test_data_set
        
        # set1 diagnostics
        if diags_set == 'set1_tables':
            try:
                seasonal_mean_table(parameter) #Calculate seasonal mean climatology
                seasonal_mean_table_html(parameter) #Generate html 
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set2_annual_cycle':
            try:
                annual_cycle_data(parameter)
                annual_cycle_line_plot(parameter)
                annual_cycle_taylor_diagram(parameter)
                annual_cycle_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set3_annual_cycle_zt': # this also include set5 diags
            try:
                annual_cycle_zt_data(parameter)
                annual_cycle_zt_plot(parameter)
                annual_cycle_zt_html(parameter)
                diurnal_cycle_zt_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set4_diurnal_cycle':
            try:
                diurnal_cycle_data(parameter)
                diurnal_cycle_plot(parameter)
                diurnal_cycle_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set6_pdf_daily':
            try:
                pdf_daily_data(parameter)
                pdf_daily_plot(parameter)
                pdf_daily_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set7_convection_onset':
            try:
                convection_onset(parameter)
                convection_onset_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set8_annual_cycle_aci':
            try:
                annual_cycle_aci_data(parameter)
                annual_cycle_aci_line_plot(parameter)
                annual_cycle_aci_taylor_diagram(parameter)
                annual_cycle_aci_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set9_aerosol_activation':
            try:
                aerosol_activation_density_plot(parameter)
                aerosol_activation_html(parameter)
                html_count = html_count + 1
            except:
                pass
         
        if diags_set == 'set10_twolegged_metric':
            try:
                twolegged_metric_plot(parameter)
                twolegged_metric_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
        if diags_set == 'set11_diurnal_cycle_LAcoupling':
            try:
                diurnal_cycle_LAcoupling_plot(parameter)
                diurnal_cycle_LAcoupling_html(parameter)
                html_count = html_count + 1
            except:
                pass
    
    #
    if html_count >= 1:
    # Create the main html page hosting all sets of diagnostics
        diags_main_html(output_path, test_model)
        #
        print(('Html files saved in:'+output_path+'/html/'))
        print(('Open Html file by (MacOS): open ' +output_path+'/html/arm_diag.html'))
        print(('Open Html file by (Linux): xdg-open ' +output_path+'/html/arm_diag.html'))
        
        print('Processes Completed!')
        print('------------------     END    -------------------------')
    else:
        print('Unable to process data. No diagnostic set was run and no html was generated!')
    
