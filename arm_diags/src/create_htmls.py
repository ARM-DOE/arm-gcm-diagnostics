import csv
from varid_dict import varid_longname

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




def annual_cycle_html(parameter):
    """Create set 2 diag. html hosting line plot and Taylor Diagram."""
    
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables

    var_longname = [ varid_longname[x] for x in variables]
    htmlfile = open(output_path+'/html/annual_cycle.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Annual Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        two_figs='annual_cycle_'+variable+'_2plots.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/'+variable+'_annual_cycle.png'
        fig2=output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram.png'
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="500" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')


def annual_cycle_zt_html(parameter):
    """ Create set 3 diag. html hosting contour and vertical profiles of annual cycle"""

    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables

    var_longname = [ varid_longname[x] for x in variables]

#    vas=['cl_p','T','Q']
#    vas_source=['ARSCL','Sounding','Sounding']
#    vas_long=['Cloud Fraction (%)','Temperature(C)','Specific Humidity (kg/kg)']
    seasons=['ANN','DJF','MAM','JJA','SON']
    #for va_ind in range(len(vas)-2):# at this stage for cl_p only
    for j, variable in enumerate(variables):
        htmlfile = open(output_path+'/html/AC_amip_contour.html',"w")
        htmlfile.write('<p><th><b>'+test_model+': Annual Cycle'+ '</b></th></p>')
        htmlfile.write('<table>')
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim.png'
        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')

        for si in range(len(seasons)):
           fig=output_path+'/figures/'+seasons[si]+'_'+variable+'_diff.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:

               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')


def diurnal_cycle_zt_html(parameter):
    """Create set 5 diag. html hosting contour plots of diurnal cycle"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables

    var_longname = [ varid_longname[x] for x in variables]

    htmlfile = open(output_path+'/html/DC_amip_contour.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Diurnal Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Monthly Mean</font><BR><TH ALIGN=LEFT><font color=red > Annual Mean</font>')

    for j, variable in enumerate(variables):
    #for va_ind in range(len(vas)-2):# at this stage for cl_p only
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_diurnal_clim.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_diurnal_clim.png'
        fig_obs_mon=output_path+'/figures/obs_'+variable+'_mon_diurnal_clim.png'
        fig_mod_mon=output_path+'/figures/mod_'+variable+'_mon_diurnal_clim.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod_mon+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs_mon+'> Obs.</a>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')

