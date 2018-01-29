#!/usr/bin/env python
import json
import copy
import numpy
import cdutil
import genutil
import cdms2
import MV2
import arm_parser
import glob
import os
import fnmatch
from src.seasonal_mean import seasonal_mean_table
from src.annual_cycle import annual_cycle_data
from src.annual_cycle import annual_cycle_line_plot
from src.annual_cycle import annual_cycle_taylor_diagram
from src.annual_cycle_zt import annual_cycle_zt_data
from src.annual_cycle_zt import annual_cycle_zt_plot
from src.diurnal_cycle import diurnal_cycle_data
from src.diurnal_cycle import diurnal_cycle_plot
from src.pdf_daily import pdf_daily_data
from src.pdf_daily import pdf_daily_plot
from src.create_htmls import annual_cycle_zt_html
from src.create_htmls import diurnal_cycle_zt_html
from src.create_htmls import diurnal_cycle_html
from src.create_htmls import seasonal_mean_table_html
from src.create_htmls import annual_cycle_html
from src.create_htmls import pdf_daily_html
from src.create_htmls import diags_main_html

def make_parameters(basic_parameter):
    #f_data = open('examples/diags_set1.json').read()
    #f_data = open('examples/diags_set2.json').read()
    #f_data = open('examples/diags_set3.json').read()
    #f_data = open('examples/diags_set4.json').read()
    #f_data = open('examples/diags_set6.json').read()
    #f_data = open('diags_all.json').read()
    f_data = open('test_set1.json').read()
    json_file = json.loads(f_data)

    parameters = []
    for key in json_file:
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

# Generate new case folder given case_id:
if not os.path.exists(case_id):
    os.makedirs(case_id)
    os.makedirs(os.path.join(case_id,'html'))
    os.makedirs(os.path.join(case_id,'figures'))
    os.makedirs(os.path.join(case_id,'metrics'))

# Loop through diagnostic sets prespecified from diags_sets.json
for parameter in parameters:

    diags_set = parameter.diags_set
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    print diags_set
    # set1 diagnostics
    if diags_set == 'set1_tables':
        seasonal_mean_table(parameter) #Calculate seasonal mean climatology
        seasonal_mean_table_html(parameter) #Generate html 

    if diags_set == 'set2_annual_cycle':
        annual_cycle_data(parameter)
        annual_cycle_line_plot(parameter)
        annual_cycle_taylor_diagram(parameter)
        annual_cycle_html(parameter)

    if diags_set == 'set3_annual_cycle_zt': # this also include set5 diags
        annual_cycle_zt_data(parameter)
        annual_cycle_zt_plot(parameter)
        annual_cycle_zt_html(parameter)
        diurnal_cycle_zt_html(parameter)

    if diags_set == 'set4_diurnal_cycle':
        diurnal_cycle_data(parameter)
        diurnal_cycle_plot(parameter)
        diurnal_cycle_html(parameter)

    if diags_set == 'set6_pdf_daily':
        pdf_daily_data(parameter)
        pdf_daily_plot(parameter)
        pdf_daily_html(parameter)
    
#
# Creat the main html page hosting all sets of diagnostics
diags_main_html(output_path, test_model)
#
print 'Html files saved in:'+output_path+'/html/'
print 'Open Html file by (MacOS): open ' +output_path+'/html/arm_diag.html'
print 'Open Html file by (Linux): xdg-open ' +output_path+'/html/arm_diag.html'

print 'Processes Completed!'
print '------------------     END    -------------------------'
    
    
    
    





