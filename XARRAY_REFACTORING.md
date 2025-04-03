# CDMS2 to Xarray Migration

This document tracks the progress of migrating from CDMS2/CDUTIL to Xarray in the ARM Diagnostics package.

## Completed Modules

1. `annual_cycle.py` - Refactored to use xarray instead of cdms2

## Migration Approach

Each module is being refactored individually using a script-by-script approach. After refactoring multiple modules, common utility functions will be extracted into a shared module.

### Key Transformations

For `annual_cycle.py`, the following changes were made:

1. **File Opening**
   - CDMS2: `cdms2.open(filename)`
   - Xarray: `xr.open_dataset(filename)`

2. **Annual Cycle Calculation**
   - CDMS2: 
     ```python
     cdutil.setTimeBoundsMonthly(var)
     var_season_data = cdutil.ANNUALCYCLE.climatology(var)(squeeze=1)
     ```
   - Xarray:
     ```python
     monthly_clim = da.groupby('time.month').mean(dim='time')
     ```

3. **Unit Conversion**
   - Created a `convert_units` function that applies unit conversions based on variable name

4. **Handling Missing Values**
   - CDMS2: Used masked arrays
   - Xarray: Using numpy NaN values to represent missing data

5. **Statistical Calculations**
   - Using numpy's nanmean, nanstd, etc., for calculations to handle missing values properly

### Benefits of the Migration

1. **Modern Ecosystem**: Xarray is part of the modern PyData ecosystem
2. **Better Documentation**: Xarray has more extensive and up-to-date documentation
3. **Active Development**: Xarray is actively maintained with regular updates
4. **Integration**: Better integration with other libraries like pandas, dask, and scikit-learn
5. **Labels**: Better handling of coordinate labels and metadata

## Testing Strategy

Each refactored module should be tested to ensure identical results with the original implementation:

1. Run both implementations on the same input data
2. Compare numerical results and plots
3. Verify that all metadata is preserved

## Future Work

1. Continue refactoring other modules in the src directory
2. Extract common xarray utility functions into a shared module
3. Eventually remove cdms2/cdutil dependencies completely