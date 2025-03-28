"""
ARM Diagnostics Parser Module.

This module contains the parser functionality for the ARM Diagnostics package.
"""
import os
import sys
import argparse
from . import arm_parameter
from . import basicparameter


class ARMParser:
    """Parser for ARM Diagnostics command-line arguments."""
    
    def __init__(self):
        """Initialize the ARM parser."""
        self.parser = argparse.ArgumentParser(
            description='ARM Diagnostics - Earth system model evaluation using ARM data'
        )
        self.load_default_args()
    
    def load_default_args(self, files=None):
        """Add arguments to the parser.
        
        Args:
            files: Optional list of parameter files to load
        """
        self.parser.add_argument(
            '-p', '--parameters',
            type=str,
            dest='parameters',
            help='Path to the user-defined parameter file',
            required=False)
        
        self.parser.add_argument(
            '--base_path',
            type=str,
            dest='base_path',
            help='Path to arm_diags',
            required=False)
        
        self.parser.add_argument(
            '--test_data_path',
            type=str,
            dest='test_data_path',
            help='Path to test data',
            required=False)
        
        self.parser.add_argument(
            '--obs_path',
            type=str,
            dest='obs_path',
            help='Path to ARM obs data',
            required=False)
        
        self.parser.add_argument(
            '--cmip_path',
            type=str,
            dest='cmip_path',
            help='Path to cmip data',
            required=False)
        
        self.parser.add_argument(
            '--output_path',
            type=str,
            dest='output_path',
            help='Path to output data',
            required=False)
        
        self.parser.add_argument(
            '-m', '--models',
            type=str,
            nargs='+',
            dest='models',
            help='Models to use',
            required=False)
        
        self.parser.add_argument(
            '-r', '--reference_data_set',
            type=str,
            dest='reference_data_set',
            help='List of observations or models that are used as a ' +
                 'reference against the test_data_set',
            required=False)
        
        self.parser.add_argument(
            '--reference_data_path',
            dest='reference_data_path',
            help='Path for the reference climitologies',
            required=False)
        
        self.parser.add_argument(
            '-t', '--test_data_set',
            type=str,
            dest='test_data_set',
            help='List of observations or models to test ' +
                 'against the reference_data_set',
            required=False)
        
        self.parser.add_argument(
            '-v', '--variables',
            type=str,
            dest='variables',
            help='Variables to use',
            required=False)
        
        self.parser.add_argument(
            '--sites',
            type=str,
            dest='sites',
            help='sites to be evaluated',
            required=False)
        
        self.parser.add_argument(
            '--plev',
            type=float,
            dest='plev',
            help='Selected pressure level',
            required=False)
        
        self.parser.add_argument(
            '-s', '--season',
            type=str,
            nargs='+',
            dest='season',
            help='Season to use',
            required=False)
        
        self.parser.add_argument(
            '--case_id',
            dest='case_id',
            help='Defines a subdirectory to the metrics output, so multiple ' +
                 'cases can be compared',
            required=False)
        
        self.parser.add_argument(
            '-o', '--output_file',
            dest='output_file',
            help='Name of the output file',
            required=False)
        
        self.parser.add_argument(
            '--reference_name',
            dest='reference_name',
            help='Name of the reference variable',
            required=False)
        
        self.parser.add_argument(
            '--test_name',
            dest='test_name',
            help='Name of the test variable',
            required=False)
        
        self.parser.add_argument(
            '--diff_name',
            dest='diff_name',
            help='Name of the difference variable',
            required=False)
        
        self.parser.add_argument(
            '--main_title',
            dest='main_title',
            help='The big title that appears on the top of the graph',
            required=False)
        
        self.parser.add_argument(
            '--reference_title',
            dest='reference_title',
            help='Title for the middle graph.',
            required=False)
        
        self.parser.add_argument(
            '--test_title',
            dest='test_title',
            help='Title for the top graph',
            required=False)
        
        self.parser.add_argument(
            '--diff_title',
            dest='diff_title',
            help='Title for the bottom graph',
            required=False)
        
        self.parser.add_argument(
            '--reference_colormap',
            dest='reference_colormap',
            help='Colormap for the middle graph.',
            required=False)
        
        self.parser.add_argument(
            '--test_colormap',
            dest='test_colormap',
            help='Colormap for the top graph',
            required=False)
        
        self.parser.add_argument(
            '--diff_colormap',
            dest='diff_colormap',
            help='Colormap for the bottom graph',
            required=False)
        
        self.parser.add_argument(
            '--arm_filename',
            dest='arm_filename',
            help='Using files with ARM naming convention.',
            action='store_const',
            const=True,
            required=False)
    
    def get_parameter(self):
        """Get a parameter object populated with values from the command line.
        
        Returns:
            ARMParameter: Parameter object with values from command line
        """
        args = self.parser.parse_args()
        parameter = arm_parameter.ARMParameter()
        
        # If a parameter file is specified, load it
        if args.parameters and os.path.exists(args.parameters):
            parameter.from_file(args.parameters)
        
        # Update with command-line arguments
        parameter.from_args(args)
        
        return parameter
    
    def get_orig_parameters(self, argparse_vals_only=False):
        """Get a parameter object loaded from basicparameter.py.
        
        This method mimics the CDP functionality to maintain compatibility.
        
        Args:
            argparse_vals_only: If True, only include values from argparse
            
        Returns:
            ARMParameter: Parameter object
        """
        # Create parameter object from basicparameter.py
        param = arm_parameter.ARMParameter()
        
        # First update with default parameter values
        module_path = os.path.dirname(os.path.abspath(basicparameter.__file__))
        basicparam_path = os.path.join(module_path, "basicparameter.py")
        param.from_file(basicparam_path)
        
        # Then update with command-line arguments
        if not argparse_vals_only:
            args = self.parser.parse_args()
            param.from_args(args)
        
        return param