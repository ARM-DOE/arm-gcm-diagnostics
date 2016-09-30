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
#    print pr_cmip_JJA[mod,:]
#np.savetxt('pr_Jun_DC_model_regrid_3x3_correct.csv',pr_cmip_6[:,:],fmt='%.3f')
#np.savetxt('pr_Jul_DC_model_regrid_3x3_correct.csv',pr_cmip_7[:,:],fmt='%.3f')
#np.savetxt('pr_Aug_DC_model_regrid_3x3_correct.csv',pr_cmip_8[:,:],fmt='%.3f')
#np.savetxt('pr_JJA_DC_model_regrid_3x3_correct.csv',pr_cmip_JJA[:,:],fmt='%.3f')
        
    
#
#
##############################Process Continuous Forcing
basedir='/p/lscratchd/zhang40/ARM_data/sgp.cf/'
#file_obs=basedir+'sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.19990101.000000.cdf'
#iname=['sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.','sgp60varanarucC1.c1.']
#originally used 10 years
#iyr=['1999','2000','2001','2002','2003','2004','2005','2006','2007','2008']#,'2009','2010','2011']
iyr=['1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011']
imon=['01','02','03','04','05','06','07','08','09','10','11','12']

pr_cf=[]
pr_obs_6=np.empty([len(iyr),30,24])*np.nan
pr_obs_7=np.empty([len(iyr),31,24])*np.nan
pr_obs_8=np.empty([len(iyr),31,24])*np.nan
pr_obs_JJA=np.empty([len(iyr),24])*np.nan
for yr_ind in range(len(iyr)):
    if iyr[yr_ind]=='1999' or iyr[yr_ind]=='2000' or iyr[yr_ind]=='2001':
        iname='sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.'
        precip='Prec'
    else:
        iname='sgp60varanarucC1.c1.'
        precip='prec_srf'

    mon_ind=['06','07','08']   #For July
    for mi in range(len(mon_ind)):
        file_obs=basedir+iname+iyr[yr_ind]+mon_ind[mi]+'01.000000.cdf'
        print file_obs,iyr[yr_ind]
        try:
            fid_obs=cdms2.open(file_obs)
            pr_obs=fid_obs(precip) # mm/hr
            print pr_obs.shape
            pr_1hr=np.squeeze(pr_obs)
            pr_1hr=np.reshape(pr_1hr,(pr_1hr.shape[0]/24,24))
      
            #pr_1hr=np.mean(pr_1hr,axis=1)
            pr_obs=pr_1hr
            print pr_1hr.shape
            fid_obs.close()
#
        except:
            print "Couldn't access", file_obs
            if mon_ind[mi]=='06':
                 pr_obs=np.empty([30,24])*np.nan
            elif mon_ind[mi]=='07':
                 pr_obs=np.empty([31,24])*np.nan
            elif mon_ind[mi]=='08':
                 pr_obs=np.empty([31,24])*np.nan
    #        pr_1hr=np.NaN
            #When Continue is used here the NAN VALUE NOT WORK!
        print mon_ind[mi],pr_obs.shape
        if mon_ind[mi]=='06':
            pr_obs_6[yr_ind,:,:]=pr_obs
        elif mon_ind[mi]=='07':
            pr_obs_7[yr_ind,:,:]=pr_obs
        elif mon_ind[mi]=='08':
            pr_obs_8[yr_ind,:,:]=pr_obs
pr_6= np.nanmean(np.nanmean(pr_obs_6,axis=0),axis=0)
pr_7= np.nanmean(np.nanmean(pr_obs_7,axis=0),axis=0)
pr_8= np.nanmean(np.nanmean(pr_obs_8,axis=0),axis=0)
pr_JJA=np.empty([3,24])
pr_JJA[0,:]=pr_6
pr_JJA[1,:]=pr_7
pr_JJA[2,:]=pr_8
np.savetxt('pr_JJA_DC_obs.csv',pr_JJA[:,:],fmt='%.3f')#
