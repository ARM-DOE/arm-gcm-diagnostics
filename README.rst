.. -*- mode: rst -*-


ARM data-oriented diagnostics package for GCMs  (ARM GCM Diag)
=====================================

This Python-based diagnostics package is currently being developed by the ARM Infrastructure Team to facilitate the use of long-term high frequency measurements from the ARM program in evaluating the regional climate simulation of clouds, radiation and precipitation. This diagnostics package computes climatological means of targeted climate model simulation and generates tables and plots for comparing the model simulation with ARM observational data. The CMIP model data sets are also included in the package to enable model inter-comparison.


Important Links
===============

- Official source code repository: https://github.com/ARM-DOE/arm-gcm-diagnostics
- ARM webpage: http://www.arm.gov/data/eval/123
- Technical Report: https://github.com/ARM-DOE/arm-gcm-diagnostics/blob/master/ARM_gcm_diag_pkg_TechReport_v2.docx


Citing
======

TBD

Install
=======
The data files including observation and CMIP5 model data are available through ARM archive. The analytical codes to calculate and visualize the diagnostics results are placed via repository (arm-gcm-diagnostics) at https://github.com/ARM-DOE/

For downloading data:

- Click https://www.arm.gov/data/eval/123
- Following the Data Directory link on that page, it will lead to the area that the data files are placed. A short registration is required if you do not already have an ARM account.
- DOI for the citation of the data is 10.5439/1282169

For obtaining codes::

    git clone https://github.com/ARM-DOE/arm-gcm-diagnostics/
    

Testing
=============
A working prototype has been set up for the users to run the package out-of-the-box. In this case, all the observation and CMIP data are already placed under directoris: /ARMDiag/observation and /ARMDiag/cmip, respectively, in the format of comma-separated values (csv). The demo model data are placed under /ARMDiag/model.

To run the package, simply type in the terminal the following::

    python ARMDiag_driver.py

To view the diagnostics results:
For Mac OS::

    open <Your Directory>/ARMDiag/html/ARM_diag.html

For Linux::

    xdg-open <Your Directory>/ARMDiag/html/ARM_diag.html

Examples
=============
In this release, the package provides 6 sets of diagnostics including:

- Tables summarizing DJF, MAM, JJA, SON and Annual Mean climatology using monthly output 
- Line plots and Taylor diagrams diagnosing annual cycle using monthly output
- Contour and vertical profiles of annual cycle for quantities with vertical distribution (i.e., cloud fraction)
- Line plots of diurnal cycle for quantities without vertical distribution (i.e., precipitation)
- Contour plots of diurnal cycle for quantities with vertical distribution 
- Line plots of Probability Density Functions using daily output

Set-up new case
=================

- Follow sample codes and data file name convention to generate model data and then place the processed data in model data directory: ARMDiag/model
- Edit config.py to change model name accordingly (make sure the model name in config.gy matchs generated model data name)
- Run the package by typing::

              python ARMDiag_driver.py



Extensions and related software
===============================

Within the package, we provide several code samples (in the directory ARMDiag/samples/) for the users to pre-process their model results. Below we provide example codes to process the monthly mean model data to be evaluated into form that can be read by the package, with the assumption that model results follows CMIP5 standard output regulation and the Ultrascale Visualization Climate Data Analysis Tools (UVCDAT) package is installed.

To have UVCDAT installed please following steps provided from below link:

* `UVCDAT <https://github.com/UV-CDAT/uvcdat/wiki/install>`_ : 
  Ultrascale Visualization Climate Data Analysis Tools.

The other required dependencies to install Py-ART in addition to Python are:

* `NumPy <http://www.scipy.org>`_
* `SciPy <http://www.scipy.org>`_
* `matplotlib <http://matplotlib.org/>`_
