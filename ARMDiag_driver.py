import ARMDiag
import config
import sys,os


print '--------------------Start ------------------------------'

print 'Gathering data for metrics calculation......'


print config.modelname
pathname = os.path.dirname(sys.argv[0])        
homedir=os.path.abspath(pathname)+'/ARMDiag/'

print('full path =', os.path.abspath(pathname)) 

print '----------------Calculate Metrics for variables --------'

print 'Calculating metrics and generating plots .....'
# 1. Prepare line plots of annual cycle for set 2 diag.. 2. Prepare data for tables in the 1st set of diag..
ARMDiag.AC_mean_amip_plot.AC_mean_amip_plot()

# Prepare Taylor Diagram of annual cycle for set 2 diag..
ARMDiag.AC_mean_amip_taylorD_plot.AC_mean_amip_taylorD_plot()

# Prepare annual cycle and diurnal cycle plots of cloud fraction for set 3 and set 5 diag.
ARMDiag.AC_DC_cl_p_plot.AC_DC_cl_p_plot()

# Prepare line and harmonic Dial diagram for diurnal cycle of precipitation for set 4 diag.
ARMDiag.DC_amip_line_harmonicD_plot.DC_amip_line_harmonicD_plot()

# Prepare line plots (PDFs) of precipitation based on daily mean data for set 6 diag. 
ARMDiag.Daily_amip_PDF_plot.Daily_amip_PDF_plot()

print '----------------Creating htmls for hosting the diagonstics results --------'
# Create set 1 diag. html hosting the table summarizing DJF, MAM, JJA, SON,ANN mean climatology
ARMDiag.AC_mean_amip_table.AC_mean_amip_table()

# Create set 2 diag. html hosting line plot and Taylor Diagram. 
ARMDiag.AC_mean_amip_line_taylorD_html.AC_mean_amip_line_taylorD_html()

# Create set 3 diag. html hosting contour and vertical profiles of annual cycle
ARMDiag.AC_amip_contour_html.AC_amip_contour_html()

# Create set 4 diag. html hosting line and harmonic dial diagram for diurnal cycle of precipitation
ARMDiag.DC_mean_amip_line_harmonicD_html.DC_mean_amip_line_harmonicD_html()

# Create set 5 diag. html hosting contour plots of diurnal cycle
ARMDiag.DC_amip_contour_html.DC_amip_contour_html()

# Create set 6 diag. html hosting line plots of precipitation pdfs
ARMDiag.Daily_amip_PDF_plot_html.Daily_amip_PDF_plot_html()

# Creat the main html page hosting all sets of diagnostics
ARMDiag.write_html.write_html()

print 'Html files saved in:'+homedir+'html/'
print 'Open Html file by (MacOS): open ' +homedir+'html/ARM_diag.html'
print 'Open Html file by (Linux): xdg-open ' +homedir+'html/ARM_diag.html'

print 'Processes Completed!'
print '------------------     END    -------------------------'
