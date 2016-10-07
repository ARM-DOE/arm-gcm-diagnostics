import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

####################Process model data
#Load cloud fraction profile climatology file (.nc).
file_mod=''
f_in1=cdms2.open(file_mod)

pr1=f_in1('cl_p')
pr1[pr1>100]=np.nan
pr1_2d=np.reshape(pr1,(12,8,37))

month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

#Replace CESM1-CAM5 with your model name
with file('cl_p_CESM1-CAM5_regrid_3x3_correct.csv', 'w') as outfile:
    outfile.write('# Array shape: {0}'.format(pr1_2d.shape)+' as (month, hours, vertical levels)\n')
    mon_id=0
    for data_slice in pr1_2d:
        #outfile.write('# New slice\n')
        outfile.write('#'+month[mon_id]+' slice\n')
        np.savetxt(outfile, data_slice, fmt='%-7.2f')
        mon_id=mon_id+1
