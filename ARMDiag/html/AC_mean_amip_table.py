import os,sys
import csv

#def AC_mean_amip_table(homedir):


#    basedir='/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/html/'
pathname = os.path.dirname(sys.argv[0])
homedir=os.path.abspath(pathname)+'/ARMDiag/'


basedir=homedir
#os.chdir(basedir+'html')

#os.chdir('/Users/zhang40/Documents/ARM_LLNL/ARMDiag_v1_lite/ARMDiag/html/')
seasons=['ANN','DJF','MAM','JJA','SON']
# Open the CSV file for reading
for item in seasons:
    reader = csv.reader(open(basedir+'metrics/CESM-CAM5_cf_diff_mmm_'+item+'.csv'))
    
    # Create the HTML file for output
    htmlfile = open(basedir+'html/'+item+'_mean_table.html',"w")
    htmlfile.write('<p><th><b>'+'CESM-CAM5: '+item+'. Mean'+ '</b></th></p>')
    
    
    # initialize rownum variable
    rownum = 0
    
    space='&nbsp;'
#    header='Variables'+40*space+'Model'+10*space+'Obs'+10*space+'Model-Obs'+10*space+'CMIP5_MMM'
    header='Variables'+40*space+'Model'+10*space+'Obs'+10*space+'Model-Obs'+10*space+'CMIP5_MMM'+10*space+'RMSE'
    htmlfile.write('<th><b>'+header+ '</b></th>')
    # write <table> tag
    htmlfile.write('<table>')
    
    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','net_sfc','prw','cllvi','net_rad','net_hf','albedo']
    #vas_space=[ "{:<15}".format(x) for x in vas]
    vas=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Relative Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Net Surface Energy flux (W/m2)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Sfc. Net Radiative Flux (W/m2)','Sfc. Net SH+LF Fluxes (W/m2)','Surface Albedo']
    vas=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Surface Albedo']

    len_space=[40-len(x) for x in vas]
    vas_space=[space*x for x in len_space]
    
    # generate table contents
    for row in reader: # Read a single row from the CSV file
        htmlfile.write('<p>')
        htmlfile.write('<tr>')
        for column in row:
            htmlfile.write('<td><TH ALIGN=LEFT>' + vas[rownum]+vas_space[rownum]+'<TH ALIGN=LEFT>'+column + '</td></b>')
        htmlfile.write('</tr>')
        htmlfile.write('</p>')
    
        #increment row count    
    
        rownum += 1
    # write </table> tag
    
    htmlfile.write('</table>')

###############Main html

htmlfile = open(basedir+'html/AC_mean_amip_table.html',"w")
htmlfile.write('<p><th><b>'+'CESM-CAM5: Annual Mean and Seasonal Mean Table'+ '</b></th></p>')
htmlfile.write('<table>')
htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
htmlfile.write('<TH><BR>')
htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
htmlfile.write('<TH><BR>')
htmlfile.write('<TH ALIGN=LEFT><A HREF="ANN_mean_table.html"> ANN</a>')
htmlfile.write('<TH ALIGN=LEFT><A HREF="DJF_mean_table.html"> DJF</a>')
htmlfile.write('<TH ALIGN=LEFT><A HREF="MAM_mean_table.html"> MAM</a>')
htmlfile.write('<TH ALIGN=LEFT><A HREF="JJA_mean_table.html"> JJA</a>')
htmlfile.write('<TH ALIGN=LEFT><A HREF="SON_mean_table.html"> SON</a>')

