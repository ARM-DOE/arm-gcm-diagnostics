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
from src.create_htmls import seasonal_mean_table_html

def make_parameters(basic_parameter):
    f_data = open('diags_sets.json').read()
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
    # set1 diagnostics
    if diags_set == 'set1_tables':
        seasonal_mean_table(parameter) #Calculate seasonal mean climatology
        seasonal_mean_table_html(parameter) #Generate html 

#    if diags_set == set2_annual_cycle:
#        AC_mean_amip_plot(parameter)
#        AC_mean_amip_taylorD_plot(parameter)
#        # Create set 2 diag. html hosting line plot and Taylor Diagram. 
#        AC_mean_amip_line_taylorD_html(parameter)
#
## Creat the main html page hosting all sets of diagnostics
#write_html()
#
#print 'Html files saved in:'+basedir+'html/'
#print 'Open Html file by (MacOS): open ' +basedir+'html/ARM_diag.html'
#print 'Open Html file by (Linux): xdg-open ' +basedir+'html/ARM_diag.html'
#
#print 'Processes Completed!'
#print '------------------     END    -------------------------'
    
    
    
    





