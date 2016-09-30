import os,sys
import csv
import config

mod = config.modelname

def AC_mean_amip_line_taylorD_html():
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    
    print 'html', basedir
        
    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','ps','prw','cllvi','albedo']
    xaxis=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Surface Pressure (Pa)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Surface Albedo']
    
    htmlfile = open(basedir+'html/AC_amip_line_taylorD.html',"w")
    htmlfile.write('<p><th><b>'+mod+': Annual Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    for va_ind in range(len(vas)):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+xaxis[va_ind])
        two_figs='AC_amip_line_taylorD_'+vas[va_ind]+'_2plots.html'
        htmlfile1 = open(basedir+'html/'+two_figs,"w")
        fig1='../figures/AC_amip_'+vas[va_ind]+'.png'
        fig2='../figures/AC_amip_taylorD_'+vas[va_ind]+'.png'
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="500" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')
