import os,sys
import csv
import config

mod = config.modelname

def DC_mean_amip_line_harmonicD_html():
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    
    print 'html', basedir
        
    vas=['pr']
    xaxis=['Precipitation (mm/day)']
    month=['Jun','Jul','Aug']
    
    htmlfile = open(basedir+'html/DC_amip_line_harmonicD.html',"w")
    htmlfile.write('<p><th><b>'+mod+': Diurnal Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Line plot and Harmonic Dial</font>')

    for va_ind in range(len(vas)):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+xaxis[va_ind])
        for mon_id in range(len(month)):
            two_figs='DC_amip_line_harmonicD_'+vas[va_ind]+'_'+month[mon_id]+'_2plots.html'
            htmlfile1 = open(basedir+'html/'+two_figs,"w")
            fig1=basedir+'figures/DC_amip_'+vas[va_ind]+'_'+month[mon_id]+'_line.png'
            fig2=basedir+'figures/DC_amip_'+vas[va_ind]+'_'+month[mon_id]+'_harmonicD.png'
            htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="550" height="500"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
            htmlfile.write('<TD><A HREF='+two_figs+'>'+month[mon_id]+'.</a></TD>')
            #htmlfile.write('<><A HREF='+two_figs+'>'+month[mon_id]+'.</a>')
