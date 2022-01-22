#===========================================================================================================================
# Program for generate the HTML files hosting the results -- Original written by Dr. Chengzhu Zhang @ LLNL
#---------------------------------------------------------------------------------------------------------------------------
# V3 Development
    # ---------------------------------------------------------------------------------------
    # Xiaojian Zheng - Dec 2021
    # ### change the input/output format to site-dependent (ENA/MAO added)
    # ### fix minor issues on image linking
    # ---------------------------------------------------------------------------------------
#===========================================================================================================================
import csv
from .varid_dict import varid_longname
import os
from collections import OrderedDict

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def diags_main_html(output_path,test_model):
    """Creat the main html page hosting all sets of diagnostics"""
    #output_path = parameter.output_path
    #test_model = parameter.test_data_set
    os.chdir(output_path+'/html')
    print((os.getcwd()))
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
      <font color=blue>Basic Diagnostics Sets</font><br> 
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
    <p>
    <TD>
      <TH ALIGN=left>
      <font color=blue>Process-oriented Diagnostics Sets</font><br>
      <font color=red>1</font> <A HREF="convection_onset.html">Basic diagnostics plots</A> for Convection Onset.<br>


    </Table>

    <p>
    <p>
    <Table>
    <em>Click on Plot Type</em></b><p>
      <A HREF="annual_cycle.html"><img src="../../../arm-gcm-diagnostics/arm_diags/misc/clt_annual_cycle_sgpc1.png"  border=1 hspace=3 alt="Set 1" width="150" height="150"></a>
      <A HREF="annual_cycle.html"><img src="../../../arm-gcm-diagnostics/arm_diags/misc/clt_annual_cycle_taylor_diagram_sgpc1.png"  border=1 hspace=3 alt="Set 1" width="150" height="150"></a>
      <A HREF="annual_cycle_zt.html"><img src="../../../arm-gcm-diagnostics/arm_diags/misc/cl_p_obs_annual_cycle_clim_sgpc1.png"   border=1 hspace=3 alt="Set 3" width="150" height="150"></a>
      <A HREF="diurnal_cycle_zt.html"><img src="../../../arm-gcm-diagnostics/arm_diags/misc/cl_p_obs_diurnal_clim_sgpc1.png"   border=1 hspace=3 alt="Set 3" width="150" height="150"></a>
      <A HREF="diurnal_cycle.html"><img src="../../../arm-gcm-diagnostics/arm_diags/misc/pr_JJA_diurnal_cycle_sgpc1.png"   border=1 hspace=3 alt="Set 4" width="150" height="150"></a>
      <A HREF="pdf_daily.html"><img src="../../../arm-gcm-diagnostics/arm_diags/misc/pr_JJA_pdf1_daily_sgpc1.png"   border=1 hspace=3 alt="Set 6" width="150" height="150"></a>
    
    </TH>
    </TD>
    
    </TR>
    </TABLE>
    
    </TD>
    <Table>
    <img src="../../../arm-gcm-diagnostics/arm_diags/misc/ARM_DIAGS_logo.png" >
    </TABLE>
    
    
    </html>"""

    f.write(message)
    f.close()
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
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
            reader = csv.reader(open(output_path+'/metrics/'+site+'/'+'seasonal_mean_table_'+ season +'_' + site+'.csv'))
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
    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'seasonal_mean_table_{}_sgpc1.html'
    title_to_file['North Slope of Alaska (NSA)'] = 'seasonal_mean_table_{}_nsac1.html'
    title_to_file['Eastern North Atlantic (ENA)'] = 'seasonal_mean_table_{}_enac1.html'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'seasonal_mean_table_{}_twpc1.html'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'seasonal_mean_table_{}_twpc2.html'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'seasonal_mean_table_{}_twpc3.html'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'seasonal_mean_table_{}_maom1.html'
    
    with open(output_path + '/html/seasonal_mean_table.html', 'w') as htmlfile:
    #test_model = 'something'
    #with open('seasonal_mean_table.html', 'w') as htmlfile:
        htmlfile.write('<p><th><b>'+test_model+': Annual Mean and Seasonal Mean Table'+ '</b></th></p>')
        htmlfile.write('<table>')
    
        for title in title_to_file:
            htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
            htmlfile.write('<TH><BR>')
            htmlfile.write('<TR><TH ALIGN=LEFT>Annual and seasonal mean tables')
            htmlfile.write('<TH><BR>')
            for season in ['ANN', 'DJF', 'MAM', 'JJA', 'SON']:
                file_name = title_to_file[title].format(season)
                htmlfile.write('<TH ALIGN=LEFT><A HREF="{}"> {}</a>'.format(file_name, season))
            htmlfile.write('<tr><td><br/></td></tr>')
    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
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

    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'sgpc1'
    title_to_file['North Slope of Alaska (NSA)'] = 'nsac1'
    title_to_file['Eastern North Atlantic (ENA)'] = 'enac1'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'twpc1'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'twpc2'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'twpc3'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'maom1'


    for title in title_to_file:
        title_name=title_to_file[title]
        htmlfile.write('<tr><td><br/></td></tr>')
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
        for j, variable in enumerate(variables):
            # Create the HTML file for output
            htmlfile.write('<TH><BR>')
            htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
            two_figs='annual_cycle_'+variable+'_2plots_{}.html'.format(title_name)
            htmlfile1 = open(output_path+'/html/'+two_figs,"w")
            fig1=output_path+'/figures/{}/'.format(title_name)+variable+'_annual_cycle_{}.png'.format(title_name)
            fig2=output_path+'/figures/{}/'.format(title_name)+variable+'_annual_cycle_taylor_diagram_{}.png'.format(title_name)
            htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="550" height="450"></div><div style="float:left"><img src='+fig2+' alt="Line" width="500" height="450"></div>')
            htmlfile.write('<TH ALIGN=LEFT><A HREF='+two_figs+'>Line plot and Taylor Diagram.</a>')
    htmlfile.write('<tr><td><br/></td></tr>')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def annual_cycle_zt_html(parameter):
    """ Create set 3 diag. html hosting contour and vertical profiles of annual cycle"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables

    var_longname = [ varid_longname[x] for x in variables]

    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'sgpc1'
    title_to_file['North Slope of Alaska (NSA)'] = 'nsac1'
    title_to_file['Eastern North Atlantic (ENA)'] = 'enac1'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'twpc1'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'twpc2'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'twpc3'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'maom1'

#    vas=['cl_p','T','Q']
#    vas_source=['ARSCL','Sounding','Sounding']
#    vas_long=['Cloud Fraction (%)','Temperature(C)','Specific Humidity (kg/kg)']
    seasons=['ANN','DJF','MAM','JJA','SON']
    #for va_ind in range(len(vas)-2):# at this stage for cl_p only
    for j, variable in enumerate(variables):
        htmlfile = open(output_path+'/html/annual_cycle_zt.html',"w")
        htmlfile.write('<p><th><b>'+test_model+': Annual Cycle'+ '</b></th></p>')
        htmlfile.write('<table>')
        
        for title in title_to_file:
            htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
            #htmlfile.write('<TH><BR>')
            htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')

            htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
            title_name = title_to_file[title]
            fig_obs=output_path+'/figures/{}/'.format(title_name)+variable+'_obs_annual_cycle_clim_{}.png'.format(title_name)
            fig_mod=output_path+'/figures/{}/'.format(title_name)+variable+'_mod_annual_cycle_clim_{}.png'.format(title_name)
            fig_diff=output_path+'/figures/{}/'.format(title_name)+variable+'_diff_annual_cycle_clim_{}.png'.format(title_name)
            htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
            htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
            htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
            #htmlfile.write('<TH><BR>')

            for si in range(len(seasons)):
               fig=output_path+'/figures/{}/'.format(title_name)+variable+'_diff_'+seasons[si]+'_{}.png'.format(title_name)
               if seasons[si]=='ANN':
                   htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
               else:
                   htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')
            htmlfile.write('<tr><td><br/></td></tr>')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def diurnal_cycle_html(parameter):
    """Create set 4 diag. html hosting line and harmonic dial diagram for diurnal cycle of precipitation"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables
    seasons = parameter.season
    sites = parameter.sites

    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'sgpc1'
    title_to_file['North Slope of Alaska (NSA)'] = 'nsac1'
    title_to_file['Eastern North Atlantic (ENA)'] = 'enac1'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'twpc1'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'twpc2'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'twpc3'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'maom1'

    var_longname = [ varid_longname[x] for x in variables]

    htmlfile = open(output_path+'/html/diurnal_cycle.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Diurnal Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')

    for title in title_to_file:
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Line plot and Harmonic Dial</font>')
        title_name = title_to_file[title]
        for j, variable in enumerate(variables):
            # Create the HTML file for output
            #htmlfile.write('<TH><BR>')
            htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
            for season in seasons:
                two_figs='diurnal_cycle_'+variable+'_'+season+'_2plots_{}.html'.format(title_name)
                htmlfile1 = open(output_path+'/html/'+two_figs,"w")
                fig1=output_path+'/figures/{}/'.format(title_name)+variable+'_'+season+'_diurnal_cycle_{}.png'.format(title_name)
                fig2=output_path+'/figures/{}/'.format(title_name)+variable+'_'+season+'_diurnal_cycle_harmonic_diagram_{}.png'.format(title_name)
                htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="600" height="500"></div><div style="float:left"><img src='+fig2+' alt="Line" width="550" height="450"></div>')
                htmlfile.write('<TD><A HREF='+two_figs+'>'+season+'.</a></TD>')
        htmlfile.write('<tr><td><br/></td></tr>')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def diurnal_cycle_zt_html(parameter):
    """Create set 5 diag. html hosting contour plots of diurnal cycle"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables

    var_longname = [ varid_longname[x] for x in variables]

    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'sgpc1'
    title_to_file['North Slope of Alaska (NSA)'] = 'nsac1'
    title_to_file['Eastern North Atlantic (ENA)'] = 'enac1'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'twpc1'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'twpc2'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'twpc3'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'maom1'

    htmlfile = open(output_path+'/html/diurnal_cycle_zt.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Diurnal Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    for title in title_to_file:
        title_name = title_to_file[title]
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Monthly Mean</font><BR><TH ALIGN=LEFT><font color=red > Annual Mean</font>')
    
        for j, variable in enumerate(variables):
        #for va_ind in range(len(vas)-2):# at this stage for cl_p only
            htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])#+'('+vas_source[va_ind]+')')
            fig_obs=output_path+'/figures/{}/'.format(title_name)+variable+'_obs_diurnal_clim_{}.png'.format(title_name)
            fig_mod=output_path+'/figures/{}/'.format(title_name)+variable+'_mod_diurnal_clim_{}.png'.format(title_name)
            fig_obs_mon=output_path+'/figures/{}/'.format(title_name)+variable+'_obs_mon_diurnal_clim_{}.png'.format(title_name)
            fig_mod_mon=output_path+'/figures/{}/'.format(title_name)+variable+'_mod_mon_diurnal_clim_{}.png'.format(title_name)
            htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod_mon+'> Model</a>')
            htmlfile.write('<A HREF='+fig_obs_mon+'> Obs.</a>')
            htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
            htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def pdf_daily_html(parameter):
    """Create set 6 diag. html hosting line plots of precipitation pdfs"""

    output_path = parameter.output_path
    test_model = parameter.test_data_set
    variables = parameter.variables
    seasons = parameter.season

    var_longname = [ varid_longname[x] for x in variables]

    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'sgpc1'
    title_to_file['North Slope of Alaska (NSA)'] = 'nsac1'
    title_to_file['Eastern North Atlantic (ENA)'] = 'enac1'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'twpc1'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'twpc2'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'twpc3'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'maom1'

    htmlfile = open(output_path+'/html/pdf_daily.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Probability Density Function Based on Daily Mean'+ '</b></th></p>')
    htmlfile.write('<table>')

    for title in title_to_file:
        title_name = title_to_file[title]
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Line plot</font>')
    
        for j, variable in enumerate(variables):
            # Create the HTML file for output
            htmlfile.write('<TH><BR>')
            htmlfile.write('<TR><TH ALIGN=LEFT>'+var_longname[j])
            for season in seasons:
                two_figs='pdf_daily_'+variable+'_'+season+'_2plots_{}.html'.format(title_name)
                htmlfile1 = open(output_path+'/html/'+two_figs,"w")
                fig1=output_path+'/figures/{}/'.format(title_name)+variable+'_'+season+'_pdf1_daily_{}.png'.format(title_name)
                fig2=output_path+'/figures/{}/'.format(title_name)+variable+'_'+season+'_pdf2_daily_{}.png'.format(title_name)
                htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="600" height="500"></div><div style="float:left"><img src='+fig2+' alt="Line" width="600" height="500"></div>')
                htmlfile.write('<TD><A HREF='+two_figs+'>'+season+'.</a></TD>')
        htmlfile.write('<tr><td><br/></td></tr>')

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def convection_onset_html(parameter):
    """Create set 5 diag. html hosting contour plots of diurnal cycle"""
    output_path = parameter.output_path
    test_model = parameter.test_data_set

    title_to_file = OrderedDict()
    title_to_file['Southern Great Plains (SGP)'] = 'sgpc1'
    title_to_file['Eastern North Atlantic (ENA)'] = 'enac1'
    #title_to_file['North Slope of Alaska (NSA)'] = 'nsac1'
    title_to_file['Tropical Western Pacific (TWP), Manus, Papua New Guinea'] = 'twpc1'
    title_to_file['Tropical Western Pacific (TWP), Nauru Island'] = 'twpc2'
    title_to_file['Tropical Western Pacific (TWP), Darwin, Australia'] = 'twpc3'
    #    title_to_file['Niamey ARM Mobile Facility'] = 'nim'
    title_to_file['Manacapuru (MAO), Amazonas, Brazil'] = 'maom1'
   

    htmlfile = open(output_path+'/html/convection_onset.html',"w")
    htmlfile.write('<p><th><b>'+test_model+': Convection Onset'+ '</b></th></p>')
    htmlfile.write('<table>')
    for title in title_to_file:
        title_name = title_to_file[title]
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>{}</font><TH><BR><TR>'.format(title))
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=black >convection onset diagnostics</font><BR><TH ALIGN=LEFT><font color=red ></font>')

        two_figs='convection_onset_'+title_name+'_2plots.html'
        htmlfile1 = open(output_path+'/html/'+two_figs,"w")
        fig1=output_path+'/figures/{}/'.format(title_name)+'conv_diagnostics_{}_{}.png'.format(test_model, title_name)
        fig2=output_path+'/figures/{}/'.format(title_name)+'conv_diagnostics_ARM_{}.png'.format(title_name)
        htmlfile1.write('<div class="container"><div style="float:left"><img src='+fig1+' alt="Line" width="700" height="250"></div><div style="float:left"><img src='+fig2+' alt="Line" width="700" height="250"></div>')
        htmlfile.write('<TD><A HREF='+two_figs+'>'+'model vs. obs'+'</a></TD>')
