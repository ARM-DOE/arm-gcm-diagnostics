.. -*- mode: rst -*-


ARM data-oriented diagnostics package for GCMs  (ARM GCM Diag)
=====================================

This Python-based diagnostics package is currently being developed by the ARM Infrastructure Team to facilitate the use of long-term high frequency measurements from the ARM program in evaluating the regional climate simulation of clouds, radiation and precipitation. This diagnostics package computes climatological means of targeted climate model simulation and generates tables and plots for comparing the model simulation with ARM observational data. The CMIP model data sets are also included in the package to enable model inter-comparison.


Important Links
===============

- Official source code repository: https://github.com/ARM-DOE/arm-gcm-diagnostics
- ARM webpage: https://www.arm.gov/data/data-sources/adcme-123 (Click Data Directory for data)
- Repository traffic statistics: https://arm-doe.github.io/arm-gcm-diagnostics/traffic-report/ (Updated weekly)


References
======
Overview of the ARM-Diags:

- Zhang, C., S. Xie, C. Tao, S. Tang, T. Emmenegger, J. D. Neelin, K. A. Schiro, W. Lin, and Z. Shaheen. "The ARM Data-oriented Metrics and Diagnostics Package for Climate Models-A New Tool for Evaluating Climate Models with Field Data."     Bulletin of the American Meteorological Society (2020). 

- Technical report, 2024: "ARM Data-Oriented Metrics and DiagnosticsPackage (ARM-Diags) for Climate Model Evaluation" https://portal.nersc.gov/project/capt/ARMVAP/ARM_DIAG_v4.pdf

- Presentation at ARM/ASR meeting 2020: "ARM Data-Oriented Diagnostics to Evaluate the Climate Model Simulation" https://asr.science.energy.gov/meetings/stm/presentations/2020/976.pdf

- Presentation at ARM/ASR meeting 2023: "Overview of ARM diagnostic package (ARM-Diags) and its applications to climate model evaluation" https://asr.science.energy.gov/meetings/stm/presentations/2023/1576.pdf

Applications of the ARM-Diags:

- Zhang, C., S. Xie, S. A. Klein, H.-Y. Ma, S. Tang, K. V. Weverberg, C. Morcrette, and J. Petch (2018), CAUSES: Diagnosis of the summertime warm bias in CMIP5 climate models at the ARM Southern Great Plains site, Journal of Geophysical Research: Atmospheres, 123(6), doi:10.1002/2017JD027200.
- Emmenegger, T., Y. Kuo, S. Xie, C. Zhang, C. Tao, and J. D. Neelin, 2022: Evaluating Tropical Precipitation Relations in CMIP6 Models with ARM Data. J. Climate, 35, 6343–6360, https://doi.org/10.1175/JCLI-D-21-0386.1. 
- Zheng, X., C. Tao, C. Zhang, S. Xie, Y. Zhang, B. Xi, and X. Dong, 2023: Assessment of CMIP5 and CMIP6 AMIP Simulated Clouds and Surface Shortwave Radiation Using ARM Observations over Different Climate Regions. J. Climate, 36, 8475–8495, https://doi.org/10.1175/JCLI-D-23-0247.1. 
- Emmenegger, T., F. Ahmed, Y. Kuo, S. Xie, C. Zhang, C. Tao, and J. D. Neelin, 2024: The Physics behind Precipitation Onset Bias in CMIP6 Models: The Pseudo-Entrainment Diagnostic and Trade-Offs between Lapse Rate and Humidity. J. Climate, 37, 2013–2033, https://doi.org/10.1175/JCLI-D-23-0227.1. 

Installation
============

The ARM Diagnostics package can be installed using conda, pip, or from source. The package requires Python 3.6 or later.

Data files including observation and CMIP model data are available through the ARM archive:

- Visit the ARM Data Center: https://www.arm.gov/data/data-sources/adcme-123 
- Follow the Data Directory link on that page to access the data files
- A short registration is required if you do not already have an ARM account
- DOI for the citation of the data is 10.5439/1646838

Installation with conda
----------------------

To create a conda environment with all the required dependencies::
    
    conda create -n arm_diags_env python=3.8
    conda activate arm_diags_env
    conda install -c conda-forge numpy scipy matplotlib xarray xcdat pandas netCDF4

After setting up the conda environment, you can install the package using the conda recipe::

    cd arm-gcm-diagnostics/conda
    conda build .
    conda install --use-local arm_diags

Installation with pip
--------------------

You can install the latest release of ARM Diagnostics using pip::

    pip install arm-diags

Installation from source
-----------------------

For development or the latest features, you can install directly from the GitHub repository::

    git clone https://github.com/ARM-DOE/arm-gcm-diagnostics/
    cd arm-gcm-diagnostics
    pip install -e .

Usage
=====

Command-line Interface
---------------------

ARM Diagnostics now provides a user-friendly command-line interface. After installation, you can run diagnostics using the `arm-diags` command::

    arm-diags run --config /path/to/config.json --output /path/to/output

For more options::

    arm-diags --help

Testing
-------

A test case has been set up for users to run the package out-of-the-box. For this test:

1. Download the observation, CMIP data, and test data from the ARM archive and place them under these directories::

    <data_directory>/observation
    <data_directory>/cmip6
    <data_directory>/testmodel

2. Run the package using the provided example configuration::

    # Set environment variables for data paths
    export ARM_DIAGS_BASE_PATH=/path/to/data_directory
    
    # Run diagnostics with an example configuration
    arm-diags run --config /path/to/arm-gcm-diagnostics/arm_diags/examples/diags_all_multisites_v3_cmip6_annual.json

3. View the diagnostics results:

   For macOS::

     open /path/to/output/html/arm_diag.html

   For Linux::

     xdg-open /path/to/output/html/arm_diag.html


Examples
=============
In this release, the following sets of diagnostics are included:

- Tables summarizing DJF, MAM, JJA, SON and Annual Mean climatology using monthly output 
- Line plots and Taylor diagrams diagnosing annual cycle using monthly output
- Contour and vertical profiles of annual cycle for quantities with vertical distribution (i.e., cloud fraction)
- Line and harmonic dial plots of the diurnal cycle of precipitation
- Line plots of Probability Density Functions (PDF) using daily output
- Line plots of the diurnal cycle for quantities relevant to the land-atmosphere coupling (e.g.,sensible and latent heat flux, PBL) 
- Convection onset metrics showing the statistical relationship between precipitation rate and column water vapor
- Aerosol-CCN activation metrics describing the percentage distribution of how many aerosols can be activated as CCN under different supersaturation levels
- Two-legged metrics evaluating the strength of L-A coupling by partitioning the impact of the land states on surface fluxes (the land leg) and from the impact of surface fluxes on the atmospheric states (the atmospheric leg)

Clike `here <https://portal.nersc.gov/project/capt/ARMVAP/arm_diag_v4_example.html>`_ for an example of the ARM-Diags v4. Please refer to the `technical report <https://github.com/UV-CDAT/uvcdat/wiki/install>`_ for more details.

Setting Up a New Analysis
=======================

Using Custom Model Data
-----------------------

1. To use CMIP output provided within the ARM dataset:
   - Copy the CMIP model data from the ARM archive to your local data directory

2. To use your own model output:
   - Save your model data in the appropriate directory structure
   - Files should follow CMIP naming conventions for compatibility
   - Ensure proper formatting following the examples in the test data

3. Create a configuration file:
   - Use one of the example JSON files in the `arm_diags/examples/` directory as a template
   - Modify parameters to match your analysis requirements

4. Run the diagnostics with your configuration:

   Using environment variables::

       # Set environment variables
       export ARM_DIAGS_TEST_MODEL="your_model_name"
       export ARM_DIAGS_CASE_ID="your_analysis_name"
       export ARM_DIAGS_BASE_PATH="/path/to/your/data"
       
       # Run diagnostics
       arm-diags run --config /path/to/your/config.json

   Or specify paths directly::

       arm-diags run --config /path/to/your/config.json --output /path/to/output



Dependencies
============

ARM Diagnostics relies on the following key packages:

* `numpy <https://numpy.org/>`_: Scientific computing with Python
* `scipy <https://scipy.org/>`_: Scientific computing library for Python
* `matplotlib <https://matplotlib.org/>`_: Visualization with Python
* `xarray <https://xarray.dev/>`_: N-D labeled arrays and datasets
* `xcdat <https://xcdat.readthedocs.io/>`_: Climate data analysis built on xarray
* `pandas <https://pandas.pydata.org/>`_: Data analysis and manipulation tool
* `netCDF4 <https://unidata.github.io/netcdf4-python/>`_: Python interface to the netCDF C library

Other useful tools in the Earth science ecosystem:

* `CDAT <https://github.com/CDAT>`_: Climate Data Analysis Tools
* `xarray <https://xarray.dev/>`_: N-D labeled arrays and datasets
* `ESMValTool <https://www.esmvaltool.org/>`_: Earth System Model Evaluation Tool
