import sys
import csv
import os

pathname = os.path.dirname(sys.argv[0])
homedir=os.path.abspath(pathname)+'/'
basedir=homedir
os.chdir(basedir)


vas=['cl','T','Q']   
vas_source=['ARSCL','Sounding','Sounding']   
vas_long=['Cloud Fraction (%)','Temperature(C)','Specific Humidity (kg/kg)']   
#vas=['tas','pr']

#htmlfile = open('AC_amip_'+vas[va_ind]+'.html',"w")
htmlfile = open('DC_amip_contour.html',"w")
htmlfile.write('<p><th><b>'+'CESM-CAM5: Diurnal Cycle'+ '</b></th></p>')
htmlfile.write('<table>')
htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
#htmlfile.write('<TH><BR>')
htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Monthly Mean</font><BR><TH ALIGN=LEFT><font color=red > Annual Mean</font>')

#htmlfile.write('</table>')
#htmlfile.write('<table>')
for va_ind in range(len(vas)):
    # Create the HTML file for output
#  /g/g92/zhang40/calc_stats/figures/
#    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>'+vas_long[va_ind]+'('+vas_source[va_ind]+')')
    #htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/CFMIP2_EC-EARTH_cl_mon_diurnal_clim.png"> Model</a>')
    htmlfile.write('<A HREF="../figures/ARSCL_cl_mon_diurnal_clim.png"> Obs.</a>')
    #htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/CFMIP2_EC-EARTH_cl_diurnal_clim.png"> Model</a>')
    htmlfile.write('<A HREF="../figures/ARSCL_cl_diurnal_clim.png"> Obs.</a>')
#    htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_'+vas[va_ind]+'.png"> Line plot.</a>')
#    htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_taylorD_'+vas[va_ind]+'.png">Taylor Diagram.</a>')
   
    
    
#    # initialize rownum variable
#    rownum = 0
#    
#    space='&nbsp;'
#    header='Variables'+30*space+'Model'+15*space+'Obs'+10*space+'Model-Obs'+5*space+'CMIP5_MMM'
#    htmlfile.write('<th><b>'+header+ '</b></th>')
#    # write <table> tag
#    htmlfile.write('<table>')
#    
#    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','net_sfc','prw','cllvi','net_rad','net_hf','albedo']
#    #vas_space=[ "{:<15}".format(x) for x in vas]
#    vas=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Relative Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Net Surface Energy flux (W/m2)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Sfc. Net Radiative Flux (W/m2)','Sfc. Net SH+LF Fluxes (W/m2)','Surface Albedo']
#    len_space=[40-len(x) for x in vas]
#    vas_space=[space*x for x in len_space]
#    
#    # generate table contents
#    for row in reader: # Read a single row from the CSV file
#        htmlfile.write('<p>')
#        htmlfile.write('<tr>')
#        for column in row:
#            htmlfile.write('<td><b>' + vas[rownum]+vas_space[rownum]+column + '</td></b>')
#        htmlfile.write('</tr>')
#        htmlfile.write('</p>')
#    
#        #increment row count    
#    
#        rownum += 1
#    # write </table> tag
#    
#    htmlfile.write('</table>')
