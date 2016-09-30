import os,sys
import config

mod = config.modelname

def AC_amip_contour_html():
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    
    vas=['cl_p','T','Q']   
    vas_source=['ARSCL','Sounding','Sounding']   
    vas_long=['Cloud Fraction (%)','Temperature(C)','Specific Humidity (kg/kg)']   
    seasons=['ANN','DJF','MAM','JJA','SON']
    for va_ind in range(len(vas)-2):# at this stage for cl_p only
        htmlfile = open(basedir+'html/AC_amip_contour.html',"w")
        htmlfile.write('<p><th><b>'+mod+': Annual Cycle'+ '</b></th></p>')
        htmlfile.write('<table>')
        htmlfile.write('<TR><TH ALIGN=LEFT><BR><TH ALIGN=LEFT><font color=blue size=+1>Southern Great Plains (SGP)</font><TH><BR><TR>')
        #htmlfile.write('<TH><BR>')
        htmlfile.write('<TR><TH><BR><TH ALIGN=LEFT><font color=red >Contour plots</font><BR><TH ALIGN=LEFT><font color=red > Vertical profiles</font>')
        
        htmlfile.write('<TR><TH ALIGN=LEFT>'+vas_long[va_ind]+'('+vas_source[va_ind]+')')
        fig_obs=basedir+'figures/obs_'+vas[va_ind]+'_annual_cycle_clim.png'
        fig_mod=basedir+'figures/mod_'+vas[va_ind]+'_annual_cycle_clim.png'
        fig_diff=basedir+'figures/diff_'+vas[va_ind]+'_annual_cycle_clim.png'
        htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig_mod+'> Model</a>')
        htmlfile.write('<A HREF='+fig_obs+'> Obs.</a>')
        htmlfile.write('<A HREF='+fig_diff+'> Model-Obs.</a>')
        #htmlfile.write('<TH><BR>')
        
        for si in range(len(seasons)):
           fig=basedir+'figures/'+seasons[si]+'_'+vas[va_ind]+'_diff.png'
           if seasons[si]=='ANN':
               htmlfile.write('<TH ALIGN=LEFT><A HREF='+fig+'> '+seasons[si]+'</a>')
           else:
               
               htmlfile.write('<A HREF='+fig+'> '+seasons[si]+'</a>')
