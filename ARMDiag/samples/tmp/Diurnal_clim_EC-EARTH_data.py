import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
from cdms2 import MV2
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure, show, rc, grid
import numpy as np
import numpy.ma as ma
####################OBS data
#basedir='/p/lscratchd/zhang40/ARM_data/sgp.c1/stats/'
basedir='/g/g92/zhang40/calc_stats/repo/ARMDiag_nc/ARMDiag/observation/'
file_obs=basedir+'ARMdiag_c1_diurnal_climo_plev_1997.nc'
####################Model data
#basedir1='/p/lscratchd/zhang40/ARM_data/CFMIP2/'
basedir1='/g/g92/zhang40/calc_stats/repo/ARMDiag_nc/ARMDiag/model/'
file_mod=basedir1+'CFMIP2_EC-EARTH_cl_clim.nc'
f_in=cdms2.open(file_obs)
f_in1=cdms2.open(file_mod)

pr=f_in('cl_p')
pr1=f_in1('cl_p')
pr[pr<0]=np.nan
pr1[pr1>100]=np.nan
pr_2d=np.reshape(pr,(12,24,37))
pr1_2d=np.reshape(pr1,(12,8,37))

print pr_2d[0,0,0]
print pr1_2d[0,0,0]
month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
with file('cl_p_obs.csv', 'w') as outfile:
    outfile.write('# Array shape: {0}'.format(pr_2d.shape)+' as (month, hours, vertical levels)\n')
    mon_id=0
    for data_slice in pr_2d:
        #outfile.write('# New slice\n')
        outfile.write('#'+month[mon_id]+' slice\n')
        np.savetxt(outfile, data_slice, fmt='%-7.2f')
        mon_id=mon_id+1
with file('cl_p_CESM1-CAM5_regrid_3x3_correct.csv', 'w') as outfile:
    outfile.write('# Array shape: {0}'.format(pr1_2d.shape)+' as (month, hours, vertical levels)\n')
    mon_id=0
    for data_slice in pr1_2d:
        #outfile.write('# New slice\n')
        outfile.write('#'+month[mon_id]+' slice\n')
        np.savetxt(outfile, data_slice, fmt='%-7.2f')
        mon_id=mon_id+1
