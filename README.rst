.. -*- mode: rst -*-


ARM data-oriented diagnostics package for GCMs  (ARM GCM Diag)
=====================================

This Python-based diagnostics package is currently being developed by the ARM Infrastructure Team to facilitate the use of long-term high frequency measurements from the ARM program in evaluating the regional climate simulation of clouds, radiation and precipitation. This diagnostics package computes climatological means of targeted climate model simulation and generates tables and plots for comparing the model simulation with ARM observational data. The CMIP model data sets are also included in the package to enable model inter-comparison.


Important Links
===============

- Official source code repository: https://github.com/ARM-DOE/arm-gcm-diagnostics
- ARM webpage: http://www.arm.gov/data/eval/123  (v2 data are under ARM data review, will soon available March/April 2020)
- Technical Report: https://github.com/ARM-DOE/arm-gcm-diagnostics/blob/master/ARM_gcm_diag_pkg_TechReport_v1.docx


References
======

Zhang, C., S. Xie, S. A. Klein, H.-Y. Ma, S. Tang, K. V. Weverberg, C. Morcrette, and J. Petch (2018), CAUSES: Diagnosis of the summertime warm bias in CMIP5 climate models at the ARM Southern Great Plains site, Journal of Geophysical Research: Atmospheres, 123(6), doi:10.1002/2017JD027200.

Install
=======

The data files including observation and CMIP5 model data are available through ARM archive. The analytical codes to calculate and visualize the diagnostics results are placed via repository (arm-gcm-diagnostics) at https://github.com/ARM-DOE/

For downloading data:

- Click https://www.arm.gov/data/eval/123
- Following the Data Directory link on that page, it will lead to the area that the data files are placed. A short registration is required if you do not already have an ARM account.
- DOI for the citation of the data is 10.5439/1282169

For obtaining codes::

    git clone https://github.com/ARM-DOE/arm-gcm-diagnostics/
    
To create conda enviroment (for a minimum enviroment)::
    
    conda create -n arm_diags_env_py2 cdp=1.0.3 cdutil cdms2 libcdms matplotlib scipy python=2 -c conda-forge -c uvcdat
    
To activate the conda enviroment::
    
    conda activate arm_diags_env

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
In this release, the package provides 6 sets of diagnostics including:

- Tables summarizing DJF, MAM, JJA, SON and Annual Mean climatology using monthly output 
- Line plots and Taylor diagrams diagnosing annual cycle using monthly output
- Contour and vertical profiles of annual cycle for quantities with vertical distribution (i.e., cloud fraction)
- Line plots of diurnal cycle for quantities without vertical distribution (i.e., precipitation)
- Contour plots of diurnal cycle for quantities with vertical distribution 
- Line plots of Probability Density Functions using daily output

For now, the diagnostics focus over SGP site. And in a later release we will include data and diagnostics for more ARM site.

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
