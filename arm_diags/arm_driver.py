#!/usr/bin/env python
"""
ARM Diagnostics Driver Module.

This module contains the core functionality for running the ARM Diagnostics package.
"""

import json
import copy
import numpy as np
import xarray as xr
import xcdat
import shutil
import glob
import os
import pdb
import fnmatch
import pandas as pd
from .src.dataset import open_dataset, climatology
from .src.core import climo, get_diurnal_cycle, var_annual_cycle
from . import arm_parser
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
    annual_cycle_zt_html, diurnal_cycle_zt_html, diurnal_cycle_html,
    seasonal_mean_table_html, annual_cycle_html, annual_cycle_aci_html,
    pdf_daily_html, convection_onset_html, aerosol_activation_html,
    twolegged_metric_html, diurnal_cycle_LAcoupling_html, diags_main_html
)


def make_parameters(basic_parameter, config_file=None):
    """
    Create parameter objects from the configuration file.
    
    Args:
        basic_parameter: The basic parameter object with default values
        config_file: Path to the configuration file (JSON format)
    
    Returns:
        list: A list of parameter objects
    """
    if config_file is None:
        config_file = 'diags_all_multisites_for_cmip6.json'
    
    with open(config_file, 'r') as f:
        f_data = f.read()
    
    json_file = json.loads(f_data)
    
    parameters = []
    for key in json_file:
        print((json_file[key], key))
        for single_run in json_file[key]:
            p = copy.deepcopy(basic_parameter)
            for attr_name in single_run:
                setattr(p, attr_name, single_run[attr_name])
            parameters.append(p)
    
    return parameters


def process_diagnostics(parameters, basic_parameter):
    """
    Process diagnostics for each parameter set.
    
    Args:
        parameters: List of parameter objects
        basic_parameter: The basic parameter object with default values
    
    Returns:
        int: 0 on success, 1 on failure
    """
    case_id = basic_parameter.case_id
    output_path = basic_parameter.output_path
    armdiags_path = basic_parameter.armdiags_path
    print('output_path: ', output_path)
    
    # Generate new case folder given case_id:
    if not os.path.exists(os.path.join(output_path)):
        os.makedirs(output_path)
        os.makedirs(os.path.join(output_path, 'html'))
        os.makedirs(os.path.join(output_path, 'figures'))
        os.makedirs(os.path.join(output_path, 'metrics'))
    
    # Copy the logo figures to the newly created html folder
    # Get the directory of the current module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    misc_dir = os.path.join(current_dir, 'misc')
    dst = os.path.join(output_path, 'html')
    
    if os.path.exists(misc_dir):
        src = os.listdir(misc_dir)
        for ifile in range(len(src)):
            src1 = os.path.join(misc_dir, src[ifile])
            shutil.copy(src1, dst)
    else:
        # Fallback to the old method for compatibility
        src = os.listdir(armdiags_path + 'arm_diags/misc/')
        dst = output_path + '/html/'
        for ifile in range(len(src)):
            src1 = armdiags_path + 'arm_diags/misc/' + src[ifile]
            shutil.copy(src1, dst)
    
    # Loop through diagnostic sets prespecified from diags_sets.json
    html_count = 0
    for parameter in parameters:
        diags_set = parameter.diags_set
        output_path = parameter.output_path
        test_model = parameter.test_data_set
        
        # set1 diagnostics
        if diags_set == 'set1_tables':
            try:
                seasonal_mean_table(parameter)  # Calculate seasonal mean climatology
                seasonal_mean_table_html(parameter)  # Generate html
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set1_tables: {e}")
        
        if diags_set == 'set2_annual_cycle':
            try:
                annual_cycle_data(parameter)
                annual_cycle_line_plot(parameter)
                annual_cycle_taylor_diagram(parameter)
                annual_cycle_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set2_annual_cycle: {e}")
        
        if diags_set == 'set3_annual_cycle_zt':  # this also include set5 diags
            try:
                annual_cycle_zt_data(parameter)
                annual_cycle_zt_plot(parameter)
                annual_cycle_zt_html(parameter)
                diurnal_cycle_zt_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set3_annual_cycle_zt: {e}")
        
        if diags_set == 'set4_diurnal_cycle':
            try:
                diurnal_cycle_data(parameter)
                diurnal_cycle_plot(parameter)
                diurnal_cycle_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set4_diurnal_cycle: {e}")
        
        if diags_set == 'set6_pdf_daily':
            try:
                pdf_daily_data(parameter)
                pdf_daily_plot(parameter)
                pdf_daily_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set6_pdf_daily: {e}")
        
        if diags_set == 'set7_convection_onset':
            try:
                convection_onset(parameter)
                convection_onset_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set7_convection_onset: {e}")
        
        if diags_set == 'set8_annual_cycle_aci':
            try:
                annual_cycle_aci_data(parameter)
                annual_cycle_aci_line_plot(parameter)
                annual_cycle_aci_taylor_diagram(parameter)
                annual_cycle_aci_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set8_annual_cycle_aci: {e}")
        
        if diags_set == 'set9_aerosol_activation':
            try:
                aerosol_activation_density_plot(parameter)
                aerosol_activation_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set9_aerosol_activation: {e}")
        
        if diags_set == 'set10_twolegged_metric':
            try:
                twolegged_metric_plot(parameter)
                twolegged_metric_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set10_twolegged_metric: {e}")
        
        if diags_set == 'set11_diurnal_cycle_LAcoupling':
            try:
                diurnal_cycle_LAcoupling_plot(parameter)
                diurnal_cycle_LAcoupling_html(parameter)
                html_count = html_count + 1
            except Exception as e:
                print(f"Error processing set11_diurnal_cycle_LAcoupling: {e}")
    
    if html_count >= 1:
        # Create the main html page hosting all sets of diagnostics
        diags_main_html(output_path, test_model)
        
        print('Html files saved in: ' + output_path + '/html/')
        print('Open Html file by (MacOS): open ' + output_path + '/html/arm_diag.html')
        print('Open Html file by (Linux): xdg-open ' + output_path + '/html/arm_diag.html')
        
        print('Processes Completed!')
        print('------------------     END    -------------------------')
        return 0
    else:
        print('Unable to process data. No diagnostic set was run and no html was generated!')
        return 1


def main():
    """Main function when module is run directly."""
    parser = arm_parser.ARMParser()
    basic_parameter = parser.get_orig_parameters(argparse_vals_only=False)
    
    # Use a default configuration file
    config_file = 'diags_all_multisites_for_cmip6.json'
    
    parameters = make_parameters(basic_parameter, config_file)
    return process_diagnostics(parameters, basic_parameter)


if __name__ == "__main__":
    main()
