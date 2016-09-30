import ARMDiag
import config
import sys,os


print '--------------------Start ------------------------------'

print 'Gathering data for metrics calculation......'

#homedir='/Users/zhang40/Documents/ARM_LLNL/ARMDiag_v1_lite/ARMDiag/'

print config.modelname
pathname = os.path.dirname(sys.argv[0])        
homedir=os.path.abspath(pathname)+'/ARMDiag/'

print('full path =', os.path.abspath(pathname)) 

#model data saved in moddir
#moddir=homedir+'model/' 

#print '----------------Calculate Metrics for variables --------'

#print 'Calculating metrics......'
#ARMDiag.AC_Mean_amip_data.AC_Mean_amip_data()#.compute_metrics(homedir)
ARMDiag.AC_mean_amip_plot.AC_mean_amip_plot()#.compute_metrics(homedir)
ARMDiag.AC_mean_amip_taylorD_plot.AC_mean_amip_taylorD_plot()#.compute_metrics(homedir)
#print 'Figures saved in:'+homedir+'figures/'
#
ARMDiag.AC_mean_amip_table.AC_mean_amip_table()#.AC_mean_amip_table(homedir)
ARMDiag.AC_DC_cl_p_plot.AC_DC_cl_p_plot()
ARMDiag.AC_amip_contour_html.AC_amip_contour_html()
ARMDiag.DC_amip_contour_html.DC_amip_contour_html()
ARMDiag.DC_amip_line_harmonicD_plot.DC_amip_line_harmonicD_plot()
ARMDiag.DC_mean_amip_line_harmonicD_html.DC_mean_amip_line_harmonicD_html()
ARMDiag.Daily_amip_PDF_plot.Daily_amip_PDF_plot()
ARMDiag.Daily_amip_PDF_plot_html.Daily_amip_PDF_plot_html()

##print '--------------------Create HTMLs------------------------'
#print 'Creating html files......'
ARMDiag.write_html.write_html()
##ARMDiag.write_html
print 'Html files saved in:'+homedir+'html/'
print 'Open Html file by (MacOS): open ' +homedir+'html/ARM_diag.html'
print 'Open Html file by (Linux): xdg-open ' +homedir+'html/ARM_diag.html'

print 'Processes Completed!'
print '------------------     END    -------------------------'
