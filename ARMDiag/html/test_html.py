import webbrowser
##############################################
f=open('set1/ARSCL_cl_mon_diurnal_clim.html','w')
#message = """<html>
# <figure>
#  <img src="/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/figures/ARSCL_cl_anual_cycle_clim.png" alt="ARSCL_cl_mon_diurnal_clim" width="304" height="228">
#</figure>
#</html>"""
#message = """<html>
#<div style="float:left;">
#<img src="../figures/ARSCL_cl_mon_diurnal_clim.png"  width="700" height="500" /><img src="../figures/CFMIP2_EC-EARTH_cl_mon_diurnal_clim.png" width="700" height="500" />
#</div>
#</html>"""
message = """<html>
<div style="float:left;">
<img src="/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/figures/ARSCL_cl_mon_diurnal_clim.png"  width="700" height="500" /><img src="/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/figures/CFMIP2_EC-EARTH_cl_mon_diurnal_clim.png" width="700" height="500" />
</div>
</html>"""

f.write(message)
f.close()

##############################################
f=open('set1/mon_diurnal_clim.html','w')
message = """<html>
<HEAD>
<TITLE>ARM Diagnostic Plots</TITLE>
</HEAD>
<b>DIAG Set 1 - Vertical contour plots of monthly means</b>
<hr noshade size=2 size="100%">
<TABLE>
<TR>
      <TH><BR>
      <TH ALIGN=LEFT><font color=blue size=+1>ARSCL Cloud Fraction</font>
    <TR>
    <TH ALIGN=LEFT>Pressure level cl
    <TH ALIGN=LEFT>Monthly mean diurnal cycle
    <TH ALIGN=LEFT><A HREF="../../figures/ARSCL_cl_mon_diurnal_clim.png"> obs.</a>
    <TH ALIGN=LEFT><A HREF="../../figures/CFMIP2_EC-EARTH_cl_mon_diurnal_clim.png">model</a>
    <TR>
<TR>
  <TH><BR>
<TR>
</TABLE>

</html>"""

f.write(message)
f.close()


f=open('set1/ARSCL_cl_mon_diurnal_clim.html','w')
#message = """<html>
# <figure>
#  <img src="/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/figures/ARSCL_cl_anual_cycle_clim.png" alt="ARSCL_cl_mon_diurnal_clim" width="304" height="228">
#</figure>
#</html>"""
#message = """<html>
#<div style="float:left;">
#<img src="../figures/ARSCL_cl_mon_diurnal_clim.png"  width="700" height="500" /><img src="../figures/CFMIP2_EC-EARTH_cl_mon_diurnal_clim.png" width="700" height="500" />
#</div>
#</html>"""
message = """<html>
<div style="float:left;">
<img src="/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/figures/ARSCL_cl_mon_diurnal_clim.png"  width="700" height="500" /><img src="/g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/figures/CFMIP2_EC-EARTH_cl_mon_diurnal_clim.png" width="700" height="500" />
</div>
</html>"""

f.write(message)
f.close()


filename = 'file:///g/g92/zhang40/calc_stats/ARMDiag/ARMDiag/html/set1/' + 'mon_diurnal_clim.html'

webbrowser.open_new_tab(filename)
