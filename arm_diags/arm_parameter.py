"""
ARM Diagnostics Parameter Module.

This module contains the parameter class for the ARM Diagnostics package.
"""
from __future__ import print_function
import sys
import os
import argparse


class ARMParameter:
    """Parameter class for ARM Diagnostics.
    
    This class holds all the parameters used by the ARM Diagnostics package.
    """
    
    def __init__(self):
        """Initialize default parameter values."""
        # Basic paths and identifiers
        self.case_id = ''
        self.reference_data_path = ''
        self.test_data_path = ''
        self.obs_path = ''
        self.cmip_path = ''
        self.output_path = ''
        self.reference_data_set = ''
        self.test_data_set = ''
        
        # Analysis parameters
        self.variables = ''
        self.season = ''
        self.sites = ''
        self.regrid_tool = 'esmf'
        self.regrid_method = 'linear'
        self.output_file = 'output.png'
        
        # Plot options
        self.main_title = 'Main Title'
        
        self.test_name = ''
        self.test_title = 'Reference'
        self.test_colormap = ''
        self.test_levels = []
        self.test_units = ''
        
        self.reference_name = ''
        self.reference_title = 'Observation'
        self.reference_colormap = ''
        self.reference_levels = []
        self.reference_units = ''
        
        self.diff_name = ''
        self.diff_title = 'Model - Observation'
        self.diff_colormap = ''
        self.diff_levels = []
        self.diff_units = ''
        
        self.canvas_size_w = 1212
        self.canvas_size_h = 1628
        self.arrows = True
        self.logo = True
        self.arm_filename = True
    
    def check_values(self):
        """Check that required parameters are set."""
        if self.test_data_path == '':
            print('test_data_path is needed! Define it in the parameter file or in the command line using --test_data_path')
            sys.exit(1)
        
        return True
    
    def from_args(self, args):
        """Update parameters from command-line arguments.
        
        Args:
            args: Parsed command-line arguments
            
        Returns:
            self: Updated parameter object
        """
        # Convert args namespace to a dictionary
        if args is None:
            return self
            
        args_dict = vars(args)
        
        # Update attributes that exist in args
        for key, value in args_dict.items():
            if value is not None:  # Only override if value is provided
                if hasattr(self, key):
                    setattr(self, key, value)
        
        return self
    
    def from_file(self, parameter_file):
        """Load parameters from a Python file.
        
        Args:
            parameter_file: Path to a Python file with parameter definitions
            
        Returns:
            self: Updated parameter object
        """
        if not os.path.exists(parameter_file):
            print(f"Parameter file not found: {parameter_file}")
            return self
            
        # Execute the Python file and get variables defined in it
        parameter_dict = {}
        with open(parameter_file) as f:
            exec(f.read(), globals(), parameter_dict)
        
        # Update object attributes from the parameter file
        for key, value in parameter_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        return self