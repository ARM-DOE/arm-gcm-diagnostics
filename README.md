# Introduction

A Python-based diagnostics package is currently being developed by the ARM Infrastructure Team (PI Shaocheng Xie) to facilitate the use of long-term high frequency measurements from the ARM program in evaluating the regional climate simulation of clouds, radiation and precipitation. This diagnostics package computes climatological means of targeted climate model simulation (i.e., ACME) and generates tables and plots for comparing the model simulation with ARM observational data. The CMIP model data sets are also included in the package to enable model inter-comparison.

Basic performance metrics are computed to measure the accuracy of mean state and variability of climate models. The evaluated physical quantities include cloud fraction, temperature, relative humidity, cloud liquid water path, total column water vapor, precipitation, sensible and latent heat fluxes and radiative fluxes, with plan to extend to more fields, such as, aerosol and microphysics properties. Process-oriented diagnostics focusing on individual cloud and precipitation-related phenomena are also being developed for the evaluation and development of specific model physical parameterizations.

# Install and setup
cd /home/user/ ARMDiag_v1/

python setup.py install --user (No admin privilege is required) 

Edit ARMDiag_driver.py to modify home directory,etc.

#Pre-Process model data
We provide example codes to process the monthly mean model data to be evaluated into form that can be read by the package (refer to ARM Diag v1 User’s Guide.doc), with the assumption that model results follows CMIP5 standard output regulation and the Climate Data Analysis Tools (CDAT) package is installed.

