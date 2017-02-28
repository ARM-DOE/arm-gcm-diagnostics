import csv

def seasonal_mean_table_html(parameter):
    """Create set 1 diag. html hosting the table summarizing DJF, MAM, JJA, SON,ANN mean climatology"""
    
#    seasons=['ANN','DJF','MAM','JJA','SON']
    seasons = parameter.season
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    # Open the CSV file for reading
    for season in seasons:
        reader = csv.reader(open(output_path+'/metrics/seasonal_mean_table_'+season+'.csv'))
        # Create the HTML file for output
        htmlfile = open(output_path+'/html/seasonal_mean_table_'+season+'.html',"w+")
        htmlfile.write('<p><th><b>'+test_model+': '+season+'. Mean'+ '</b></th></p>')
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
                htmlfile.write('<tr><div style="width: 50px" >')
                #htmlfile.write('<tr>')    
                for column in row:
                    htmlfile.write('<td>' + column +'</td>')
                #htmlfile.write('</tr>')
                htmlfile.write('</div></tr>')
             #increment row count 
             rownum += 1
      # write </table> tag
        htmlfile.write('</table>') 
   
   ###############Main html
    
    htmlfile = open(output_path+'/html/seasonal_mean_table.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Annual Mean and Seasonal Mean Table'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_ANN.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_DJF.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_MAM.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_JJA.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_SON.html"> SON</a>')

