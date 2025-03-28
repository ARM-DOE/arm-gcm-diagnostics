#===========================================================================================================================
# Functions for calculate annual/seasonal cycle from monthly data -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Nov2021
    # ### Add the array treatment: filled the output masked (missing) value with numpy NaN
    # ### to avoid the issue of plotting masked value as 0 value in the plotting code
    # ---------------------------------------------------------------------------------------
# V4 Development
    # ---------------------------------------------------------------------------------------
    # 2024
    # ### Replaced cdms2/cdutil with xarray and xcdat for modern compatibility (similar to E3SM Diagnostics)
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================

"""
DEPRECATED: This module's functions have been moved to core.py

This file is maintained for backward compatibility, but all functions
have been migrated to the core.py module.
"""

# Import from core.py for backward compatibility
from .core import climo, get_diurnal_cycle, var_annual_cycle

# Alias get_diurnal_cycle_seasons to the core function for backward compatibility
get_diurnal_cycle_seasons = get_diurnal_cycle