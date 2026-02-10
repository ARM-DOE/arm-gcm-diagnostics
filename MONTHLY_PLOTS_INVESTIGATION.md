# Investigation: Missing Monthly Mean Diurnal Cycle Plots in v4

## Issue Summary

Monthly mean diurnal cycle plots for cloud fraction (12-panel grid showing each month) are reported as missing in v4, with only the annual aggregated diurnal cycle plot (single panel) being generated.

## Investigation Scope

This document provides a comprehensive analysis of the `annual_cycle_zt_plot()` function to identify why monthly plots may not be generated.

---

## Code Analysis

### File Location
`/arm_diags/src/annual_cycle_zt.py`

### Function: `annual_cycle_zt_plot()`
Lines: 165-580

### Plot Generation Sections

#### 1. Monthly Mean Diurnal Cycle Plots (Lines 265-342)
**Purpose:** Generate 12-panel grid showing diurnal cycle for each month

**Output Files:**
- `cl_p_mon_diurnal_clim_obs_{site}.png` (observations)
- `cl_p_mon_diurnal_clim_mod_{site}.png` (model)

**Key Code:**
```python
# Plot monthly mean diurnal cycle contours
for iid, index in enumerate(index_list):
    # Create figure with 4x3 subplots
    fig1, axs = plt.subplots(4, 3, figsize=(15, 12), ...)
    
    # Create a subplot for each month
    for imon in range(12):
        # Plot data for this month
        obs_data_con = np.concatenate((obs_data[imon, :, :], obs_data[imon, :, :]), axis=0)
        im = axs[imon].contourf(y, x, obs_data_con[locoff:locoff+24, ::-1], ...)
```

#### 2. Annual Aggregated Diurnal Cycle Plots (Lines 364-424)
**Purpose:** Generate single-panel plot showing annual mean diurnal cycle

**Output Files:**
- `cl_p_diurnal_clim_obs_{site}.png` (observations)
- `cl_p_diurnal_clim_mod_{site}.png` (model)

**Key Code:**
```python
# Plot diurnal cycle contours
for iid, index in enumerate(index_list):
    fig2 = plt.figure()
    # Use annual-averaged data
    obs_data_con = np.concatenate((cl_ob_diurnal, cl_ob_diurnal), axis=0)
    im = ax.contourf(y, x, obs_data_con[locoff:locoff+24, ::-1], ...)
```

---

## Code Structure Issue

### Variable Scoping Pattern

```python
# Lines 200-235: Data processing loop
for j, variable in enumerate(variables):
    if test_findex == 1:
        # Load and process test model data
        test_data = np.loadtxt(test_data_file)
        test_data = test_data.reshape((12, tlen_testVar, 37))
        cl_p = np.nanmean(test_data, axis=1)
        cl_p_diurnal = np.nanmean(test_data, axis=0)
    
    # Load and process observation data
    obs_data = np.loadtxt(obs_data_file)
    obs_data = obs_data.reshape((12, 24, 37))
    cl_ob = np.nanmean(obs_data, axis=1)
    cl_ob_diurnal = np.nanmean(obs_data, axis=0)

# Lines 237-342: Monthly plot generation (OUTSIDE loop)
# Uses: obs_data, test_data, variable

# Lines 344-424: Aggregated plot generation (OUTSIDE loop)
# Uses: cl_ob_diurnal, cl_p_diurnal
```

### Why This Matters

1. **Current Configuration:** `variables = ["cl_p"]` (single variable)
   - Loop runs once
   - After loop: `variable = "cl_p"`, `obs_data` and `test_data` contain correct data
   - Monthly and aggregated plots should both generate

2. **Potential Future Issue:** If `variables = ["cl_p", "other_var"]` (multiple variables)
   - Loop runs twice
   - After loop: `variable = "other_var"`, `obs_data` and `test_data` from "other_var"
   - Only "other_var" plots would be generated, not "cl_p"

3. **Error Handling:** If data loading fails (line 235: `continue`)
   - Variables may be undefined or contain wrong data
   - Lines 257-261 could fail when accessing `obs_data.flatten()`

---

## Root Cause Hypotheses

### Most Likely: Runtime Error in Data Processing

**During xarray refactoring (commit 686a183), data handling changed from CDMS2 to xarray.**

Potential failure points:

1. **Data Shape Mismatch**
   ```python
   # Line 227
   obs_data = obs_data.reshape((12, 24, 37))
   ```
   If loaded data doesn't have exactly `12*24*37 = 10,656` elements, reshape will fail.

2. **Array Indexing Error**
   ```python
   # Line 284-285
   obs_data_con = np.concatenate((obs_data[imon, :, :], obs_data[imon, :, :]), axis=0)
   im = axs[imon].contourf(y, x, obs_data_con[locoff:locoff+24, ::-1], ...)
   ```
   If `obs_data` has wrong shape or `locoff` is out of bounds, indexing will fail.

3. **Undefined Variables**
   ```python
   # Line 257
   ct_up = np.nanmax(obs_data.flatten())
   ```
   If `obs_data` is undefined (because loop failed), this will raise `NameError`.

### Alternative: Silent Failure

The outer try-except block (lines 177-580) will:
```python
except Exception as e:
    print(f"Error in annual_cycle_zt_plot: {e}")
    traceback.print_exc()
    raise
```

This should make failures visible. However, if:
- Error occurs between lines 342-343 (after monthly plots, before aggregated plots)
- Only monthly plot generation fails but aggregated succeeds

Then: Aggregated plots would be created, but monthly plots would not.

---

## Expected vs. Actual Behavior

### Expected Behavior (v3)
✓ Generate monthly mean diurnal cycle plots (12 panels)
✓ Generate annual aggregated diurnal cycle plots (single panel)
✓ Both plot types displayed in HTML

### Reported Behavior (v4)
✗ Monthly mean diurnal cycle plots missing
✓ Annual aggregated diurnal cycle plots generated
? Plot files may not exist or may not be linked in HTML

---

## Diagnostic Steps

### Step 1: Verify File Generation
Check if monthly plot files actually exist:
```bash
# Look for monthly plots
ls -lh <output_path>/figures/sgpc1/*mon_diurnal_clim*.png

# Look for aggregated plots  
ls -lh <output_path>/figures/sgpc1/*_diurnal_clim*.png
```

**If monthly files exist:** Issue is with HTML generation or linking
**If monthly files don't exist:** Issue is with plot generation code

### Step 2: Check Runtime Logs
Look for error messages:
- "Error processing observation data for cl_p"
- "Error in annual_cycle_zt_plot"
- Tracebacks mentioning lines 237-342

### Step 3: Validate Input Data
Check CSV input files:
```bash
# Check observation data
wc -l <output_path>/metrics/sgpc1/cl_p_obs_diurnal_climo_sgpc1.csv
# Should have: 1 header + 12*(1 month header + 24 data lines) = 1 + 12*25 = 301 lines

# Check test model data
wc -l <output_path>/metrics/sgpc1/cl_p_test_diurnal_climo_sgpc1.csv
```

### Step 4: Add Debug Logging
Insert debug statements in `annual_cycle_zt.py`:

```python
# After line 236 (end of variable loop)
print(f"DEBUG: Finished processing variables")
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: obs_data shape = {obs_data.shape}")
print(f"DEBUG: test_data shape = {test_data.shape if test_findex else 'N/A'}")

# Before line 266 (start of monthly plot loop)
print(f"DEBUG: Starting monthly plot generation")
print(f"DEBUG: index_list = {index_list}")

# After line 342 (end of monthly plot section)
print(f"DEBUG: Finished monthly plot generation")
```

---

## Recommendations

### Immediate Actions

1. **Verify plot file existence** (answers: code vs. HTML issue)
2. **Check runtime logs** (answers: silent failure vs. visible error)
3. **Add debug logging** (pinpoints exact failure location)

### Code Improvements (Future Work)

1. **Move plotting into variable loop**
   - Ensures each variable gets its own plots
   - Makes dependencies explicit
   - Prevents scoping issues

2. **Add explicit error handling**
   ```python
   try:
       # Monthly plot generation
   except Exception as e:
       print(f"Failed to generate monthly plots: {e}")
       # Continue with other plot types
   ```

3. **Validate data shapes**
   ```python
   expected_shape = (12, 24, 37)
   if obs_data.shape != expected_shape:
       raise ValueError(f"obs_data has wrong shape: {obs_data.shape}, expected {expected_shape}")
   ```

---

## Conclusion

The monthly plot generation code **exists** and **should execute**. The most likely cause is a **runtime error** introduced during the CDAT→xarray refactoring that prevents the monthly plotting section from completing successfully.

The quickest path to resolution is:
1. Check if monthly plot files are created
2. Review logs for errors
3. Add targeted debug logging to identify failure point

Once the specific failure is identified, a minimal fix can be implemented.

---

## References

- Issue: "Missing monthly mean diurnal cycle plots for cloud fraction"
- Code file: `/arm_diags/src/annual_cycle_zt.py`
- HTML generation: `/arm_diags/src/create_htmls.py` (lines 342-379)
- Refactoring commit: 686a183 "Refactor packaging and replacing cdat with xarray"
- Config file: `/arm_diags/config/diags_all_multisites_for_cmip6.json` (set3_annual_cycle_zt)
