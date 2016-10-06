import os,sys
import csv
import config

mod = config.modelname
def AC_mean_amip_table():
    """Create set 1 diag. html hosting the table summarizing DJF, MAM, JJA, SON,ANN mean climatology"""
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    
    seasons=['ANN','DJF','MAM','JJA','SON']
    # Open the CSV file for reading
    for item in seasons:
        reader = csv.reader(open(basedir+'metrics/'+mod+'_table_'+item+'.csv'))
        # Create the HTML file for output
        htmlfile = open(basedir+'html/'+item+'_mean_amip_table.html',"w+")
        htmlfile.write('<p><th><b>'+mod+': '+item+'. Mean'+ '</b></th></p>')
        # initialize rownum variable
        rownum = 0
        # write <table> tag
        htmlfile.write('<table>')
        # generate table contents
     
        for row in reader: # Read a single row from the CSV file
        
         # write header row. assumes first row in csv contains header
             if rownum == 0:
                htmlfile.write('<tr>') # write <tr> tag
                for column in row:
                    htmlfile.write('<th>' + column +'</th>')
                htmlfile.write('</tr>')
        
          #  write all other rows 
             else:
                htmlfile.write('<tr>')    
                for column in row:
                    htmlfile.write('<td>' + column +'</td>')
                htmlfile.write('</tr>')
             #increment row count 
             rownum += 1
      # write </table> tag
        htmlfile.write('</table>') 
   
   ###############Main html
    
    htmlfile = open(basedir+'html/AC_mean_amip_table.html',"w")
    htmlfile.write('<p><th><b>'+mod+': Annual Mean and Seasonal Mean Table'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="ANN_mean_amip_table.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="DJF_mean_amip_table.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="MAM_mean_amip_table.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="JJA_mean_amip_table.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="SON_mean_amip_table.html"> SON</a>')

