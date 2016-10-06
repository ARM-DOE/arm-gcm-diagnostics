import os,sys
import csv
import config

mod = config.modelname

def Daily_amip_PDF_plot_html():
    """Create set 6 diag. html hosting line plots of precipitation pdfs"""
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    
        
    vas=['pr']
    xaxis=['Precipitation (mm/day) JJA']
    
    htmlfile = open(basedir+'html/Daily_amip_PDF.html',"w")
    htmlfile.write('<p><th><b>'+mod+': Probability Density Function Based on Daily Mean'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Line plot and Harmonic Dial</font>')

    for va_ind in range(len(vas)):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+xaxis[va_ind])
        fig1=basedir+'figures/Daily_amip_'+vas[va_ind]+'_JJA_pdf1.png'
        fig2=basedir+'figures/Daily_amip_'+vas[va_ind]+'_JJA_pdf2.png'
        htmlfile.write('<TH><TH ALIGN=LEFT><A HREF='+fig1+'> Rain Frequency</a>')
        htmlfile.write('<TH><TH ALIGN=LEFT><A HREF='+fig2+'> Rain Amount</a>')
