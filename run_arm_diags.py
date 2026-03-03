#!/usr/bin/env python
"""
Run script for ARM Diagnostics (arm_diags) package.

This script replaces the need for the basicparameter.py by providing 
command-line options to configure the diagnostics, or by loading a parameter file.
"""

import os
import sys
import argparse
import datetime
import importlib.util
from pathlib import Path

# Add the parent directory to the path so we can import arm_diags
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

from arm_diags import arm_driver

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run ARM Diagnostics",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Parameter file option (alternative to command-line arguments)
    parser.add_argument("-p", "--param-file", type=str,
                      help="Path to a Python parameter file containing configuration settings")
    
    # User ID & output options
    parser.add_argument("--case-id", type=str, 
                      default=f"arm_diags_{datetime.datetime.now().strftime('%Y%m%d')}",
                      help="Unique identifier for this run")
    
    # Dataset paths
    parser.add_argument("--base-path", type=str,
                      help="Base directory containing model and observational data")
    parser.add_argument("--test-data-path", type=str,
                      help="Path to test model data (defaults to {base_path}/testmodel)")
    parser.add_argument("--obs-path", type=str,
                      help="Path to observational data (defaults to {base_path}/observation)")
    parser.add_argument("--cmip-path", type=str,
                      help="Path to CMIP data (defaults to {base_path}/cmip6)")
    parser.add_argument("--output-path", type=str,
                      help="Path where results will be saved (defaults to {base_path}/results/{case_id})")
    
    # Model information
    parser.add_argument("--test-data-set", type=str, default="testmodel",
                      help="Name of the test model dataset")
    parser.add_argument("--test-start-year", type=int, default=1979,
                      help="Start year for test data")
    parser.add_argument("--test-end-year", type=int, default=2006,
                      help="End year for test data")
    
    # Configuration options
    parser.add_argument("--config-file", type=str, 
                      default="diags_all_multisites_for_cmip6.json",
                      help="Configuration file with diagnostics settings")
    
    # Additional options
    parser.add_argument("--arm-filename", action="store_true", default=True,
                      help="Whether to use ARM filename conventions")
    
    return parser.parse_args()

def load_parameter_file(param_file_path):
    """Load parameters from a Python file."""
    class BasicParameter(object):
        pass
    
    param_module = {}
    
    try:
        # Load the parameter file as a module
        spec = importlib.util.spec_from_file_location("param_module", param_file_path)
        param_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(param_module)
    except Exception as e:
        print(f"Error loading parameter file: {e}")
        sys.exit(1)
    
    # Create a parameter object
    basic_parameter = BasicParameter()
    
    # Required parameters
    required_params = [
        ('case_id', f"arm_diags_{datetime.datetime.now().strftime('%Y%m%d')}"),
        ('base_path', None)
    ]
    
    # Optional parameters with default values
    optional_params = [
        ('test_data_set', 'testmodel'),
        ('test_start_year', 1979),
        ('test_end_year', 2006),
        ('config_file', 'diags_all_multisites_for_cmip6.json'),
        ('arm_filename', True),
        ('test_data_path', None),
        ('obs_path', None),
        ('cmip_path', None),
        ('output_path', None)
    ]
    
    # Check required parameters
    for param_name, default_value in required_params:
        if hasattr(param_module, param_name):
            setattr(basic_parameter, param_name, getattr(param_module, param_name))
        elif default_value is not None:
            setattr(basic_parameter, param_name, default_value)
        else:
            print(f"Error: Required parameter '{param_name}' not found in parameter file")
            sys.exit(1)
    
    # Set optional parameters
    for param_name, default_value in optional_params:
        if hasattr(param_module, param_name):
            setattr(basic_parameter, param_name, getattr(param_module, param_name))
        else:
            setattr(basic_parameter, param_name, default_value)
    
    # Handle derived paths if not explicitly set
    if basic_parameter.test_data_path is None:
        basic_parameter.test_data_path = os.path.join(basic_parameter.base_path, 'testmodel')
    
    if basic_parameter.obs_path is None:
        basic_parameter.obs_path = os.path.join(basic_parameter.base_path, 'observation')
    
    if basic_parameter.cmip_path is None:
        basic_parameter.cmip_path = os.path.join(basic_parameter.base_path, 'cmip6')
    
    if basic_parameter.output_path is None:
        basic_parameter.output_path = os.path.join(basic_parameter.base_path, 'results', basic_parameter.case_id)
    
    return basic_parameter

def create_basic_parameter(args):
    """Create a parameter object from command-line arguments."""
    # Create an object to hold the parameters
    class BasicParameter(object):
        pass
    
    basic_parameter = BasicParameter()
    
    # Set attributes from arguments
    basic_parameter.case_id = args.case_id
    basic_parameter.test_data_set = args.test_data_set
    basic_parameter.test_start_year = args.test_start_year
    basic_parameter.test_end_year = args.test_end_year
    basic_parameter.arm_filename = args.arm_filename
    basic_parameter.config_file = args.config_file
    
    # Handle paths
    if args.base_path is None:
        print("Error: --base-path is required when not using a parameter file")
        sys.exit(1)
        
    basic_parameter.base_path = args.base_path
    
    if args.test_data_path:
        basic_parameter.test_data_path = args.test_data_path
    else:
        basic_parameter.test_data_path = os.path.join(args.base_path, 'testmodel')
        
    if args.obs_path:
        basic_parameter.obs_path = args.obs_path
    else:
        basic_parameter.obs_path = os.path.join(args.base_path, 'observation')
        
    if args.cmip_path:
        basic_parameter.cmip_path = args.cmip_path
    else:
        basic_parameter.cmip_path = os.path.join(args.base_path, 'cmip6')
        
    if args.output_path:
        basic_parameter.output_path = args.output_path
    else:
        basic_parameter.output_path = os.path.join(args.base_path, 'results', args.case_id)
    
    return basic_parameter

def main():
    """Main function to run the diagnostics."""
    # Parse command-line arguments
    args = parse_args()
    
    # Check if parameter file is provided
    if args.param_file:
        basic_parameter = load_parameter_file(args.param_file)
    else:
        basic_parameter = create_basic_parameter(args)
    
    # Print configuration
    print("Running ARM Diagnostics with the following configuration:")
    print(f"  Case ID:           {basic_parameter.case_id}")
    print(f"  Test dataset:      {basic_parameter.test_data_set}")
    print(f"  Years:             {basic_parameter.test_start_year}-{basic_parameter.test_end_year}")
    print(f"  Base path:         {basic_parameter.base_path}")
    print(f"  Test data path:    {basic_parameter.test_data_path}")
    print(f"  Observation path:  {basic_parameter.obs_path}")
    print(f"  CMIP path:         {basic_parameter.cmip_path}")
    print(f"  Output path:       {basic_parameter.output_path}")
    print(f"  Config file:       {basic_parameter.config_file}")
    
    # Run the diagnostics
    arm_driver.run_diagnostics(basic_parameter)

if __name__ == "__main__":
    main()
