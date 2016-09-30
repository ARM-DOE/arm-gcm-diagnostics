import os,sys
import csv

def AC_amip_line_taylorD(homedir):

#    basedir='/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/html/'
    basedir=homedir
    os.chdir(basedir+'/html')
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
        if va_ind==0:
            htmlfile1 = open('AC_amip_line_taylorD_tas_2plots.html',"w")
            htmlfile1.write('<div class="container"><div style="float:left"><img src="../figures/AC_amip_tas.png" alt="Line" width="500" height="450"></div><div style="float:left"><img src="../figures/AC_amip_taylorD_tas.png" alt="Line" width="500" height="450"></div>')
            
            htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_tas.png">Line plot.</a>')
            htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_taylorD_tas.png">Taylor Diagram.</a>')
        else:
           
            htmlfile2 = open('AC_amip_line_taylorD_pr_2plots.html',"w")
            htmlfile2.write('<div class="container"><div style="float:left"><img src="../figures/AC_amip_pr.png" alt="Line" width="500" height="450"></div><div style="float:left"><img src="../figures/AC_amip_taylorD_pr.png" alt="Line" width="500" height="450"></div>')
            htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_pr.png"> Line plot.</a>')
            htmlfile.write('<TH ALIGN=LEFT><A HREF="../figures/AC_amip_taylorD_pr.png">Taylor Diagram.</a>')
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
