#!/usr/bin/env python
"""
Command-line interface for ARM Diagnostics.

This module provides the command-line interface for running the ARM Diagnostics package.
"""

import argparse
import json
import copy
import os
import sys
from . import __version__
from .arm_driver import make_parameters, process_diagnostics

# arm_parser is only needed for certain legacy features
# It requires the 'cdp' package from conda-forge
try:
    from .arm_parser import ARMParser
    HAS_ARM_PARSER = True
except ImportError:
    HAS_ARM_PARSER = False
    ARMParser = None


def main():
    """Entry point for the arm-diags command."""
    parser = argparse.ArgumentParser(
        description="ARM Diagnostics - Earth system model evaluation using ARM data"
    )
    parser.add_argument(
        "--version", action="version", version=f"arm-diags {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run diagnostics")
    run_parser.add_argument(
        "--config", "-c", type=str, required=True,
        help="Path to the configuration file (JSON format)"
    )
    run_parser.add_argument(
        "--output_path", "-o", type=str,
        help="Output directory for results (overrides config setting)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "run":
        return run_diagnostics(args)
    
    return 0


def run_diagnostics(args):
    """Run the ARM diagnostics with the provided configuration."""
    if not os.path.exists(args.config):
        print(f"Error: Config file not found: {args.config}", file=sys.stderr)
        return 1
    
    if not HAS_ARM_PARSER:
        print("Error: The 'cdp' package is required for the CLI interface.", file=sys.stderr)
        print("Install it with: conda install -c conda-forge cdp", file=sys.stderr)
        print("Alternatively, use run_arm_diags.py which doesn't require cdp.", file=sys.stderr)
        return 1
    
    try:
        # Load the configuration file
        with open(args.config, 'r') as f:
            config_data = f.read()
        
        # Get parameters
        arm_parser = ARMParser()
        basic_parameter = arm_parser.get_orig_parameters(argparse_vals_only=False)
        
        # Override output path if specified
        if args.output_path:
            basic_parameter.output_path = args.output_path
        
        # Set the configuration file as an attribute
        basic_parameter.config_file = args.config
        
        # Run the diagnostics
        json_file = json.loads(config_data)
        parameters = []
        for key in json_file:
            print(f"Processing {key}...")
            for single_run in json_file[key]:
                p = copy.deepcopy(basic_parameter)
                for attr_name in single_run:
                    setattr(p, attr_name, single_run[attr_name])
                parameters.append(p)
        
        # Process each parameter set
        process_diagnostics(parameters, basic_parameter)
        
        print("Diagnostics completed successfully!")
        return 0
    except Exception as e:
        print(f"Error running diagnostics: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())