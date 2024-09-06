#!/usr/bin/env python
import json
import copy
import numpy
import cdutil
import genutil
import shutil
import cdms2
import MV2
import glob
import os
import pdb
import fnmatch
#from arm_diags import arm_parser # from . import arm_parser 
import arm_parser
from src.seasonal_mean import seasonal_mean_table # .src
from src.annual_cycle import annual_cycle_data, annual_cycle_line_plot, annual_cycle_taylor_diagram # .src
from src.annual_cycle_aci import annual_cycle_aci_data, annual_cycle_aci_line_plot, annual_cycle_aci_taylor_diagram
from src.annual_cycle_zt import annual_cycle_zt_data,annual_cycle_zt_plot # .src
from src.diurnal_cycle import diurnal_cycle_data,diurnal_cycle_plot # .src
from src.pdf_daily import pdf_daily_data, pdf_daily_plot # .src
from src.convection_onset_driver import convection_onset # .src
from src.aerosol_activation import aerosol_activation_density_plot # .src
from src.twolegged_metric import twolegged_metric_plot # .src
from src.diurnal_cycle_LAcoupling import diurnal_cycle_LAcoupling_plot

#from src.convection_onset_driver_todd import convection_onset
from src.create_htmls import annual_cycle_zt_html,diurnal_cycle_zt_html,diurnal_cycle_html,seasonal_mean_table_html,annual_cycle_html,annual_cycle_aci_html,pdf_daily_html,convection_onset_html,aerosol_activation_html,twolegged_metric_html,diurnal_cycle_LAcoupling_html,diags_main_html
def make_parameters(basic_parameter):
    #f_data = open('examples/diags_set3.json').read()
    #f_data = open('diags_all_multisites_for_cmip5.json').read()
    f_data = open('diags_all_multisites_for_cmip6.json').read()
    #f_data = open('diags_set10_cmip6.json').read()
    #f_data = open('diags_all_multisites_for_LAcoupling.json').read()
    #f_data = open('diags_all_multisites_check.json').read()
    json_file = json.loads(f_data)

    parameters = [] 
    for key in json_file:
        print((json_file[key],key))
        for single_run in json_file[key]:
            p = copy.deepcopy(basic_parameter)
            for attr_name in single_run:
                setattr(p, attr_name, single_run[attr_name])
            parameters.append(p)
    return parameters

# Read in specification files, including those from:
# 1. basicparameter.py
# 2. diags_sets.json

parser = arm_parser.ARMParser()
basic_parameter = parser.get_orig_parameters(argparse_vals_only=False)
#basic_parameter = parser.get_parameters()
parameters = make_parameters(basic_parameter)

case_id =  basic_parameter.case_id
output_path = basic_parameter.output_path
armdiags_path = basic_parameter.armdiags_path
print('output_path: ',output_path)

# Generate new case folder given case_id:
if not os.path.exists(os.path.join(output_path)):
    os.makedirs(output_path)
    os.makedirs(os.path.join(output_path,'html'))
    os.makedirs(os.path.join(output_path,'figures'))
    os.makedirs(os.path.join(output_path,'metrics'))

# Copy the logo figures to the newly created html folder
src = os.listdir(armdiags_path+'arm_diags/misc/')
dst = output_path+'/html/'
for ifile in range(len(src)):
    src1 = armdiags_path+'arm_diags/misc/'+src[ifile]
    shutil.copy(src1, dst)

# Loop through diagnostic sets prespecified from diags_sets.json
html_count = 0
for parameter in parameters:
    diags_set = parameter.diags_set
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    #print diags_set
    # set1 diagnostics
    if diags_set == 'set1_tables':
        try:
            seasonal_mean_table(parameter) #Calculate seasonal mean climatology
            seasonal_mean_table_html(parameter) #Generate html 
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set2_annual_cycle':
        try:
            annual_cycle_data(parameter)
            annual_cycle_line_plot(parameter)
            annual_cycle_taylor_diagram(parameter)
            annual_cycle_html(parameter)
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set3_annual_cycle_zt': # this also include set5 diags
        try:
            annual_cycle_zt_data(parameter)
            annual_cycle_zt_plot(parameter)
            annual_cycle_zt_html(parameter)
            diurnal_cycle_zt_html(parameter)
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set4_diurnal_cycle':
        try:
            diurnal_cycle_data(parameter)
            diurnal_cycle_plot(parameter)
            diurnal_cycle_html(parameter)
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set6_pdf_daily':
        try:
            pdf_daily_data(parameter)
            pdf_daily_plot(parameter)
            pdf_daily_html(parameter)
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set7_convection_onset':
        try:
            convection_onset(parameter)
            convection_onset_html(parameter)
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set8_annual_cycle_aci':
        try:
            annual_cycle_aci_data(parameter)
            annual_cycle_aci_line_plot(parameter)
            annual_cycle_aci_taylor_diagram(parameter)
            annual_cycle_aci_html(parameter)
            html_count = html_count + 1
        except:
            pass

    if diags_set == 'set9_aerosol_activation':
        #try:
        aerosol_activation_density_plot(parameter)
        aerosol_activation_html(parameter)
        html_count = html_count + 1
        #except:
            #pass
     
    if diags_set == 'set10_twolegged_metric':
        twolegged_metric_plot(parameter)
        twolegged_metric_html(parameter)
        html_count = html_count + 1     

    if diags_set == 'set11_diurnal_cycle_LAcoupling':
        diurnal_cycle_LAcoupling_plot(parameter)
        diurnal_cycle_LAcoupling_html(parameter)
        html_count = html_count + 1
          

#
if html_count >= 1:
# Creat the main html page hosting all sets of diagnostics
    diags_main_html(output_path, test_model)
    #
    print(('Html files saved in:'+output_path+'/html/'))
    print(('Open Html file by (MacOS): open ' +output_path+'/html/arm_diag.html'))
    print(('Open Html file by (Linux): xdg-open ' +output_path+'/html/arm_diag.html'))
    
    print('Processes Completed!')
    print('------------------     END    -------------------------')
else:
    print('Unable to process data. No diagnostic set was run and no html was generated!')
    
