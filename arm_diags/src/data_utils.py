"""
DEPRECATED: This module is replaced by dataset.py and core.py

This module was part of the initial xarray transition, but has been
replaced by a more comprehensive approach aligned with E3SM Diagnostics.
"""

# Import replacement modules for backward compatibility
from .dataset import open_dataset, climatology
from .core import climo, get_diurnal_cycle, var_annual_cycle

def annual_cycle_climatology(data):
    """
    Alias for var_annual_cycle.
    
    This function is maintained for backward compatibility.
    """
    return var_annual_cycle(data, ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])