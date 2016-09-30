import sys,os
import csv

#def AC_amip_html(homedir):

#    basedir='/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/html/'

pathname = os.path.dirname(sys.argv[0])
homedir=os.path.abspath(pathname)+'/'
basedir=homedir
os.chdir(basedir)
vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','net_sfc','prw','cllvi','net_rad','net_hf','albedo']
vas_long=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Relative Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Net Surface Energy flux (W/m2)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Sfc. Net Radiative Flux (W/m2)','Sfc. Net SH+LF Fluxes (W/m2)','Surface Albedo']
    
#vas=['tas','pr']

#htmlfile = open('AC_amip_'+vas[va_ind]+'.html',"w")
htmlfile = open('AC_amip_line_taylorD.html',"w")
htmlfile.write('<p><th><b>'+'CESM-CAM5: Annual Cycle'+ '</b></th></p>')
htmlfile.write('<table>')
htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
for va_ind in range(len(vas)):
    # Create the HTML file for output
#  /g/g92/zhang40/calc_stats/figures/
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>'+vas_long[va_ind])
    htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_tas.png"> Line plot.</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_taylorD_tas.png">Taylor Diagram.</a>')
