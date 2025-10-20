# ARM Diagnostics Refactoring Notes

## Overview

This document describes the refactoring changes made to the ARM Diagnostics package to modernize the codebase and improve usability. The primary goals were:

1. Remove the hard-coded path dependency (`armdiags_path`)
2. Improve the package structure and resource handling
3. Create a more user-friendly run interface
4. Update the documentation to reflect these changes

## Key Changes

### 1. Removed Hard-coded Path Requirement

- **Before**: Users needed to define an `armdiags_path` variable pointing to the code repository.
- **After**: The package uses Python's resource system (importlib.resources) to access internal files.
- **Benefits**: Allows users to install the package properly without needing to know where the code is located.

### 2. Better Organization of Configuration Files

- Created a dedicated `config` directory for standard configuration files
- Moved JSON configuration files to the appropriate directories
- Updated resource discovery code to search in multiple locations for configs

### 3. Modern Run Script

- Created a new `run_arm_diags.py` script as the main entry point
- Added support for command-line arguments with descriptive help
- Added support for parameter files with the `-p` option
- The script can now be run in two ways:
  1. With a parameter file: `./run_arm_diags.py -p examples/arm_diags_params.py`
  2. With command-line arguments: `./run_arm_diags.py --base-path /path/to/data`

### 4. Proper Package Structure

- Fixed relative imports to work correctly as an installed package
- Updated all import statements to use proper relative imports
- Created proper `__init__.py` with version and exported functions
- Made resources accessible through importlib.resources

### 5. Documentation Updates

- Updated README.rst with new installation and usage instructions
- Created example parameter file in examples directory
- Documented both command-line and parameter file approaches
- Preserved the old basicparameter.py as reference in the examples directory

## Migration Guide

For users of the previous version:

### If you were using basicparameter.py:

1. Create a new parameter file based on examples/arm_diags_params.py
2. Set the same values you were using in basicparameter.py
3. Remove the armdiags_path parameter (it's no longer needed)
4. Run with `./run_arm_diags.py -p your_params.py`

### If you were using arm_driver.py directly:

1. Switch to using run_arm_diags.py 
2. Your configuration will be easier to manage and reproduce

## Directory Structure Changes

- `/arm_diags/config/` - New directory containing default configuration files
- `/examples/` - Contains example parameter files and reference files
- `run_arm_diags.py` - New main entry point for running the diagnostics

## Technical Implementation Details

1. **Resource Access**: Used Python's importlib.resources to locate and access package resources
2. **Parameter Handling**: Created a flexible system that can load parameters from files or command-line
3. **Modular Design**: Split the functionality to make it more maintainable
4. **Improved Error Messages**: Added clearer error messages when resources cannot be found

## Known Issues

- Keyboard interrupts (Ctrl+C) might not work reliably when the diagnostic computations are running
- This is likely due to the underlying scientific libraries (cdms2, matplotlib, etc.)

## Future Improvements

Potential future enhancements to consider:

1. Further reduce dependencies on legacy packages (cdms2, cdutil)
2. Add support for more data formats (NetCDF4, xarray as primary tools)
3. Implement proper logging system
4. Add more comprehensive test suite