# Python3 
#!/usr/bin/env python
import json
import copy
import numpy
import cdutil
import genutil
import cdms2
import MV2
import glob
import os
import fnmatch
from arm_diags import arm_parser # from . import arm_parser
from src.seasonal_mean import seasonal_mean_table # .src
from src.annual_cycle import annual_cycle_data, annual_cycle_line_plot, annual_cycle_taylor_diagram #.src
from src.annual_cycle_zt import annual_cycle_zt_data,annual_cycle_zt_plot #.src
from src.diurnal_cycle import diurnal_cycle_data,diurnal_cycle_plot #.src
from src.pdf_daily import pdf_daily_data, pdf_daily_plot #.src
from src.convection_onset_driver import convection_onset #.src
# from src.convection_onset_driver_todd import convection_onset
from src.create_htmls import annual_cycle_zt_html,diurnal_cycle_zt_html,diurnal_cycle_html,seasonal_mean_table_html,annual_cycle_html,pdf_daily_html,convection_onset_html,diags_main_html

def make_parameters(basic_parameter):
    #f_data = open('examples/diags_set3.json').read()
    f_data = open('diags_all_multisites.json').read()
    #f_data = open('examples/test_convection_onset.json').read()
    #f_data = open('examples/test_convection_onset_short.json').read()
    
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
basic_parameter = parser.get_parameter()
parameters = make_parameters(basic_parameter)

case_id =  basic_parameter.case_id
output_path = basic_parameter.output_path

# Generate new case folder given case_id:
if not os.path.exists(os.path.join(output_path)):
    os.makedirs(output_path)
    os.makedirs(os.path.join(output_path,'html'))
    os.makedirs(os.path.join(output_path,'figures'))
    os.makedirs(os.path.join(output_path,'metrics'))

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
            html_count += 1
        except:
            pass

    if diags_set == 'set2_annual_cycle':
        try:
            annual_cycle_data(parameter)
            annual_cycle_line_plot(parameter)
            annual_cycle_taylor_diagram(parameter)
            annual_cycle_html(parameter)
            html_count += 1
        except:
            pass

    if diags_set == 'set3_annual_cycle_zt': # this also include set5 diags
        try:
            annual_cycle_zt_data(parameter)
            annual_cycle_zt_plot(parameter)
            annual_cycle_zt_html(parameter)
            diurnal_cycle_zt_html(parameter)
            html_count += 1
        except:
            pass

    if diags_set == 'set4_diurnal_cycle':
        try:
            diurnal_cycle_data(parameter)
            diurnal_cycle_plot(parameter)
            diurnal_cycle_html(parameter)
            html_count += 1
        except:
            pass

    if diags_set == 'set6_pdf_daily':
        try:
            pdf_daily_data(parameter)
            pdf_daily_plot(parameter)
            pdf_daily_html(parameter)
            html_count += 1
        except:
            pass

    if diags_set == 'set7_convection_onset':
        try:
            convection_onset(parameter)
            convection_onset_html(parameter)
            html_count += 1
        except:
            pass
    
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
    print('No diagnostic set was run and no html was generated')
    
   
