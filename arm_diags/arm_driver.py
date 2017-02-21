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

def make_parameters(orginal_parameter):
    f_data = open('diags_sets.json').read()
    json_file = json.loads(f_data)

    parameters = []
    for key in json_file:
        for single_run in json_file[key]:
            p = copy.deepcopy(orginal_parameter)
            for attr_name in single_run:
                setattr(p, attr_name, single_run[attr_name])
            parameters.append(p)
    return parameters

parser = arm_parser.ARMParser()
orginal_parameter = parser.get_parameter()
parameters = make_parameters(orginal_parameter)

for parameter in parameters:

    test_data_path = parameter.test_data_path
    print test_data_path

    var = parameter.variables
    season = parameter.season
    ref_models = parameter.ref_models
    diags_set = parameter.diags_set
    print var, season,ref_models,diags_set

    if diags_set == set1_tables:
        AC_mean_amip_plot(parameter)
        AC_mean_amip_table(parameter)

    if diags_set == set2_annual_cycle:
        AC_mean_amip_plot(parameter)
        AC_mean_amip_taylorD_plot(parameter)
        # Create set 2 diag. html hosting line plot and Taylor Diagram. 
        AC_mean_amip_line_taylorD_html(parameter)

# Creat the main html page hosting all sets of diagnostics
write_html()

print 'Html files saved in:'+basedir+'html/'
print 'Open Html file by (MacOS): open ' +basedir+'html/ARM_diag.html'
print 'Open Html file by (Linux): xdg-open ' +basedir+'html/ARM_diag.html'

print 'Processes Completed!'
print '------------------     END    -------------------------'
    
    
    
    





