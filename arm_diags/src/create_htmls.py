import csv
from varid_dict import varid_longname
import os

def diags_main_html(output_path,test_model):
    """Creat the main html page hosting all sets of diagnostics"""
    #output_path = parameter.output_path
    #test_model = parameter.test_data_set
    os.chdir(output_path+'/html')
    print os.getcwd()
    f = open('arm_diag.html','w')
    message = """<html>
    <head>
    <TITLE>ARM Diagnostics Plots</TITLE>
    </head>
    </table>
    </b></font>
    <p>
    <b>ARM Metrics and Diagnostics Package</b>
    <p>
    <b>Model: """+test_model+"""</b>
    <hr noshade size=2 size="100%">
    <TABLE width='1550' >
    <TR>
    <TD>
      <TH ALIGN=left VALIGN=top>
      <font color=blue>Set</font>
      <font color=blue>Description</font><br>
    <p>
      <font color=red>1</font> <A HREF="seasonal_mean_table.html">Tables</A> of DJF, MAM, JJA, SON and Annual Mean.<br>
    <p>
      <font color=red>2</font> <A HREF="annual_cycle.html">Line plots and Taylor diagrams</A> of Annual Cycle.<br>
    <p>
      <font color=red>3</font> <A HREF="annual_cycle_zt.html">Contour and Vertical profiles</A> of Annual Cycle.<br>
    <p>
      <font color=red>4</font> <A HREF="diurnal_cycle.html">Line and Harmonic Dail plots</A> of Diurnal Cycle.<br>
    <p>
      <font color=red>5</font> <A HREF="diurnal_cycle_zt.html">Contour plots</A> of Diurnal Cycle.<br>
    <p>
      <font color=red>6</font> <A HREF="pdf_daily.html">Line plots</A> of Probability Density Function.<br>
    
    </Table>

    <p>
    <p>
    <Table>
    <em>Click on Plot Type</em></b><p>
      <A HREF="annual_cycle.html"><img src="../figures/pr_annual_cycle.png"  border=1 hspace=3 alt="Set 1" width="150" height="150"></a>
      <A HREF="annual_cycle.html"><img src="../figures/pr_annual_cycle_taylor_diagram.png"  border=1 hspace=3 alt="Set 1" width="150" height="150"></a>
      <A HREF="annual_cycle_zt.html"><img src="../figures/mod_cl_p_annual_cycle_clim.png"   border=1 hspace=3 alt="Set 3" width="150" height="150"></a>
      <A HREF="DC_amip_line.html"><img src="../figures/ANN_cl_p_diff.png "   border=1 hspace=3 alt="Set 3" width="150" height="150"></a>
      <A HREF="diurnal_cycle_zt.html"><img src="../figures/obs_cl_p_diurnal_clim.png"   border=1 hspace=3 alt="Set 3" width="150" height="150"></a>
      <A HREF="pdf_daily.html"><img src="../figures/pr_JJA_pdf1_daily.png"   border=1 hspace=3 alt="Set 6" width="150" height="150"></a>
    
    </TH>
    </TD>
    
    </TR>
    </TABLE>
    
    </TD>
    <Table>
    <img src="../../misc/ARM_logo.png" >
    </TABLE>
    
    
    </html>"""

    f.write(message)
    f.close()
    

def seasonal_mean_table_html(parameter):
    """Create set 1 diag. html hosting the table summarizing DJF, MAM, JJA, SON,ANN mean climatology"""
    
#    seasons=['ANN','DJF','MAM','JJA','SON']
    seasons = parameter.season
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    sites = parameter.sites
    # Open the CSV file for reading
    for site in sites:
        for season in seasons:
            reader = csv.reader(open(output_path+'/metrics/seasonal_mean_table_'+ season +'_' + site+'.csv'))
            # Create the HTML file for output
            htmlfile = open(output_path+'/html/seasonal_mean_table_'+season+'_'+site +'.html',"w+")
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
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_ANN_sgp.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_DJF_sgp.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_MAM_sgp.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_JJA_sgp.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_SON_sgp.html"> SON</a>')
    htmlfile.write('<tr><td><br/></td></tr>')

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>North Slope of Alaska (NSA)</font><TH><BR><TR>')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_ANN_nsa.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_DJF_nsa.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_MAM_nsa.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_JJA_nsa.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_SON_nsa.html"> SON</a>')


    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Manus, Papua New Guinea</font><TH><BR><TR>')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_ANN_twpc1.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_DJF_twpc1.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_MAM_twpc1.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_JJA_twpc1.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_SON_twpc1.html"> SON</a>')

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Nauru Island</font><TH><BR><TR>')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_ANN_twpc2.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_DJF_twpc2.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_MAM_twpc2.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_JJA_twpc2.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_SON_twpc2.html"> SON</a>')


    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Darwin, Australia</font><TH><BR><TR>')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
    htmlfile.write('<TH><BR>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_ANN_twpc2.html"> ANN</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_DJF_twpc2.html"> DJF</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_MAM_twpc2.html"> MAM</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_JJA_twpc2.html"> JJA</a>')
    htmlfile.write('<TH ALIGN=LEFT><A HREF="seasonal_mean_table_SON_twpc2.html"> SON</a>')

def annual_cycle_html(parameter):
    """Create set 2 diag. html hosting line plot and Taylor Diagram."""
    
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables
    sites = parameter.sites
    # Open the CSV file for reading

    var_longname = [ varid_longname[x] for x in variables]
    htmlfile = open(output_path+'/html/annual_cycle.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Annual Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        two_figs='annual_cycle_'+variable+'_2plots_sgp.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/'+variable+'_annual_cycle_sgp.png'
        fig2=output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram_sgp.png'
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="500" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')
    htmlfile.write('<tr><td><br/></td></tr>')

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>North Slope of Alaska (NSA)</font><TH><BR><TR>')
    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        two_figs='annual_cycle_'+variable+'_2plots_nsa.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/'+variable+'_annual_cycle_nsa.png'
        fig2=output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram_nsa.png'
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="500" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')
    htmlfile.write('<tr><td><br/></td></tr>')


    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Manus, Papua New Guinea</font><TH><BR><TR>')
    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        two_figs='annual_cycle_'+variable+'_2plots_twpc1.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/'+variable+'_annual_cycle_twpc1.png'
        fig2=output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram_twpc1.png'
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="500" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')
    htmlfile.write('<tr><td><br/></td></tr>')


    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Nauru Island</font><TH><BR><TR>')

    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        two_figs='annual_cycle_'+variable+'_2plots_twpc2.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/'+variable+'_annual_cycle_twpc2.png'
        fig2=output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram_twpc2.png'
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="500" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')
    htmlfile.write('<tr><td><br/></td></tr>')

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Darwin, Australia</font><TH><BR><TR>')
    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        two_figs='annual_cycle_'+variable+'_2plots_twpc3.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/'+variable+'_annual_cycle_twpc3.png'
        fig2=output_path+'/figures/'+variable+'_annual_cycle_taylor_diagram_twpc3.png'
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
        htmlfile = open(output_path+'/html/annual_cycle_zt.html',"w")
        htmlfile.write('<p><th><b>'+test_model+': Annual Cycle'+ '</b></th></p>')
        htmlfile.write('<table>')
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim_sgp.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim_sgp.png'
        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim_sgp.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')

        for si in range(len(seasons)):
           fig=output_path+'/figures/'+seasons[si]+'_'+variable+'_diff_sgp.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:

               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')


        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>North Slope of Alaska (NSA)</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim_nsa.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim_nsa.png'
        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim_nsa.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')

        for si in range(len(seasons)):
           fig=output_path+'/figures/'+seasons[si]+'_'+variable+'_diff_nsa.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:

               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')


        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Manus, Papua New Guinea</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim_twpc1.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim_twpc1.png'
        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim_twpc1.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')

        for si in range(len(seasons)):
           fig=output_path+'/figures/'+seasons[si]+'_'+variable+'_diff_twpc1.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:

               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')


        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Nauru Island</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim_twpc2.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim_twpc2.png'
        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim_twpc2.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')

        for si in range(len(seasons)):
           fig=output_path+'/figures/'+seasons[si]+'_'+variable+'_diff_twpc2.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:

               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')

        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Darwin, Australia</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
        fig_obs=output_path+'/figures/obs_'+variable+'_annual_cycle_clim_twpc3.png'
        fig_mod=output_path+'/figures/mod_'+variable+'_annual_cycle_clim_twpc3.png'
        fig_diff=output_path+'/figures/diff_'+variable+'_annual_cycle_clim_twpc3.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')

        for si in range(len(seasons)):
           fig=output_path+'/figures/'+seasons[si]+'_'+variable+'_diff_twpc3.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:

               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')
def diurnal_cycle_html(parameter):
    """Create set 4 diag. html hosting line and harmonic dial diagram for diurnal cycle of precipitation"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables
    season = parameter.season

    var_longname = [ varid_longname[x] for x in variables]


    htmlfile = open(output_path+'/html/diurnal_cycle.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Diurnal Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Line plot and Harmonic Dial</font>')

    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        for season in season:
            two_figs='diurnal_cycle_'+variable+'_'+season+'_2plots.html'
            htmlfile1 = open(output_path+'/html/'+two_figs,"w")
            fig1=output_path+'/figures/'+variable+'_'+season+'_diurnal_cycle.png'
            fig2=output_path+'/figures/'+variable+'_'+season+'_diurnal_cycle_harmonic_diagram.png'
            htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="550" height="500"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
            htmlfile.write('<TD><A HREF='+two_figs+'>'+season+'.</a></TD>')




def diurnal_cycle_zt_html(parameter):
    """Create set 5 diag. html hosting contour plots of diurnal cycle"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables

    var_longname = [ varid_longname[x] for x in variables]

    htmlfile = open(output_path+'/html/diurnal_cycle_zt.html',"w")
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

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>North Slope of Alaska (NSA)</font><TH><BR><TR>')
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

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Manus, Papua New Guinea</font><TH><BR><TR>')
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

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Nauru Island</font><TH><BR><TR>')
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

    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Tropical Western Pacific (TWP), Darwin, Australia</font><TH><BR><TR>')
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
def pdf_daily_html(parameter):
    """Create set 6 diag. html hosting line plots of precipitation pdfs"""

    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables
    season = parameter.season

    var_longname = [ varid_longname[x] for x in variables]


    htmlfile = open(output_path+'/html/pdf_daily.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Probability Density Function Based on Daily Mean'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Line plot</font>')


    for j, variable in enumerate(variables):
        # Create the HTML file for output
        htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
        for season in season:

            two_figs='pdf_daily_'+variable+'_'+season+'_2plots.html'
            htmlfile1 = open(output_path+'/html/'+two_figs,"w")
            fig1=output_path+'/figures/'+variable+'_'+season+'_pdf1_daily.png'
            fig2=output_path+'/figures/'+variable+'_'+season+'_pdf2_daily.png'
            htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="550" height="500"></div><div style="float:left"><img src='+fig2+' alt="Line" width="550" height="500"></div>')
            htmlfile.write('<TD><A HREF='+two_figs+'>'+season+'.</a></TD>')

