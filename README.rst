.. -*- mode: rst -*-


ARM data-oriented diagnostics package for GCMs  (ARM GCM Diag)
=====================================

This Python-based diagnostics package is currently being developed by the ARM Infrastructure Team to facilitate the use of long-term high frequency measurements from the ARM program in evaluating the regional climate simulation of clouds, radiation and precipitation. This diagnostics package computes climatological means of targeted climate model simulation and generates tables and plots for comparing the model simulation with ARM observational data. The CMIP model data sets are also included in the package to enable model inter-comparison.


Important Links
===============

- Official source code repository: https://github.com/ARM-DOE/arm-gcm-diagnostics
- ARM webpage: https://www.arm.gov/data/data-sources/adcme-123 (Click Data Directory for data)


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

Install
=======

The data files including observation and CMIP5 model data are available through ARM archive. The analytical codes to calculate and visualize the diagnostics results are placed via repository (arm-gcm-diagnostics) at https://github.com/ARM-DOE/

For downloading data:

- Click https://www.arm.gov/data/data-sources/adcme-123 
- Following the Data Directory link on that page, it will lead to the area that the data files are placed. A short registration is required if you do not already have an ARM account.
- DOI for the citation of the data is 10.5439/1646838

For obtaining codes::

    git clone https://github.com/ARM-DOE/arm-gcm-diagnostics/
    
To create conda enviroment (for a minimum enviroment)::
    
    conda create -n arm_diags_env_py3 cdp cdutil cdms2 libcdms matplotlib scipy python=3 -c conda-forge -c uvcdat
    
To activate the conda enviroment::
    
    conda activate arm_diags_env_py3

To install the package, go into <Your directory> (/arm-gcm-dignostics/)::
    
    python setup.py install

Testing
=============

A test case has been set up for the users to run the package out-of-the-box. In this case, all the observation, CMIP data, test data should be downloaded placed under directoris:: 

 <Your directory>/arm_diags/observation
 <Your directory>/arm_diags/cmip
 <Your directory>/arm_diags/model

Edit parameter file basicparameter.py to set 'base_path' to <Your directory>

To run the package, simply type in the terminal the following::
   
  python arm_driver.py -p basicparameter.py

To view the diagnostics results:

For Mac OS::

  open <Your directory>/arm_diags/case_name/html/ARM_diag.html

For Linux::

   xdg-open <Your directory>/ arm_diags/case_name/html/ARM_diag.html


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

Set-up new case
=================

- To apply this package to any CMIP output provided within our dataset, just copy the CMIP model data from <Your directory>/ arm_diags /cmip to <Your directory>/ arm_diags /model.
- To apply this package to your own model output. The input datasets should be saved under data directory <Your directory>/ arm_diags /model. The file name should follow the test data files provided and the data sets should follow the CMIP convention, so that the input files are readable by the software package.
- Edit basicparameter.py as follows:
- Change 'test_data_set' to the model name
- Edit 'case_id' to create folder to save diagnostics results 
- Edit 'base_path' to spedify location of the data
- Run the package by typing::

              python arm_driver.py -p basicparameter.py



Extensions and related software
===============================

* `UVCDAT <https://github.com/UV-CDAT/uvcdat/wiki/install>`_ : 
  Ultrascale Visualization Climate Data Analysis Tools.

The other required dependencies to install Py-ART in addition to Python are:

* `NumPy <http://www.scipy.org>`_
* `SciPy <http://www.scipy.org>`_
* `matplotlib <http://matplotlib.org/>`_
