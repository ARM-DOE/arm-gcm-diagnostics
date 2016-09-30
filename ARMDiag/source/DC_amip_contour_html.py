import os,sys
import config

mod = config.modelname

def DC_amip_contour_html():
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'

    vas=['cl_p','T','Q']
    vas_source=['ARSCL','Sounding','Sounding']
    vas_long=['Cloud Fraction (%)','Temperature(C)','Specific Humidity (kg/kg)']

    htmlfile = open(basedir+'html/DC_amip_contour.html',"w")
    htmlfile.write('<p><th><b>'+mod+': Diurnal Cycle'+ '</b></th></p>')
    htmlfile.write('<table>')
    htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
    htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Monthly Mean</font><BR><TH ALIGN=LEFT><font color=red > Annual Mean</font>')

    for va_ind in range(len(vas)-2):# at this stage for cl_p only
        htmlfile.write('<TR><TH ALIGN=LEFT>'+vas_long[va_ind]+'('+vas_source[va_ind]+')')
        fig_obs=basedir+'figures/obs_'+vas[va_ind]+'_diurnal_clim.png'
        fig_mod=basedir+'figures/mod_'+vas[va_ind]+'_diurnal_clim.png'
        fig_obs_mon=basedir+'figures/obs_'+vas[va_ind]+'_mon_diurnal_clim.png'
        fig_mod_mon=basedir+'figures/mod_'+vas[va_ind]+'_mon_diurnal_clim.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod_mon+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs_mon+'> Obs.</a>')
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
   
    
    
