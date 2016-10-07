import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
from cdms2 import MV2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from scipy.optimize import curve_fit

cmipdir='/p/lscratchd/zhang40/ARM_data/sgp_cmip/'

modellist=['MIROC5','CMCC-CM','inmcm4','CCSM4','GFDL-HIRAM-C180','GFDL-HIRAM-C360','FGOALS-s2','HadGEM2-A','ACCESS1-0','ACCESS1-3']
pr_cmip_6=np.empty([len(modellist),8])
pr_cmip_7=np.empty([len(modellist),8])
pr_cmip_8=np.empty([len(modellist),8])
pr_cmip_JJA=np.empty([3,len(modellist),8])

for mod in range(len(modellist)):
    print mod, modellist[mod]
    file_mod=cmipdir+modellist[mod]+'_amip_r1i1p1_DC_regrid_3x3_v0.nc'
    f_in=cdms2.open(file_mod)
    pr=f_in('pr')  #for each model total days for 30 years of simulations are different, HadGEM simulate 360 days per year
    pr=np.squeeze(pr)  
    #Convert from kg/m2/s to mm/day
    if modellist[mod]=='HadGEM2-A':
        pr=pr[:83520]*3600*24  #get first  29 years 
        print pr.shape
        pr_yr=np.mean(np.reshape(pr,(29,360,8)),axis=0)
        pr_6=np.mean(pr_yr[153:183,:],axis=0)
        pr_7=np.mean(pr_yr[183:214,:],axis=0)
        pr_8=np.mean(pr_yr[214:245,:],axis=0)
        
    else:
        pr= pr[:84680]*3600*24  #get first  29 years    
        print pr.shape
        pr_yr=np.mean(np.reshape(pr,(29,365,8)),axis=0)
        pr_6=np.mean(pr_yr[150:180,:],axis=0)
        pr_7=np.mean(pr_yr[180:210,:],axis=0)
        pr_8=np.mean(pr_yr[210:240,:],axis=0)
    pr_cmip_6[mod,:]=pr_6
    pr_cmip_7[mod,:]=pr_7
    pr_cmip_8[mod,:]=pr_8
pr_cmip_JJA[0,:,:]=pr_cmip_6
pr_cmip_JJA[1,:,:]=pr_cmip_7
pr_cmip_JJA[2,:,:]=pr_cmip_8
month=['Jun','Jul','Aug']
with file('pr_JJA_DC_model_regrid_3x3_correct.csv', 'w') as outfile:
    outfile.write('# Array shape: {0}'.format(pr_cmip_JJA.shape)+' as (month, models, hours)\n')
    mon_id=0
    for data_slice in pr_cmip_JJA:
        #outfile.write('# New slice\n')
        outfile.write('#'+month[mon_id]+' slice\n')
        np.savetxt(outfile, data_slice, fmt='%-7.3f')
        mon_id=mon_id+1
