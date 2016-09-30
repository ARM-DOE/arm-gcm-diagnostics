import os,sys
import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
import matplotlib.pyplot as plt
import numpy as np

def AC_mean_amip_data():
    pathname = os.path.dirname(sys.argv[0])
    print os.path.abspath(pathname)
    homedir=os.path.abspath(pathname)+'/ARMDiag/'
    basedir=homedir
    print 'blabla'
    
    basedir1='/p/lscratchd/zhang40/ARM_data/sgp.cf/stats/'
    basedir2='/p/lscratchd/zhang40/ARM_data/sgp.c1/stats/'
    cmipdir='/p/lscratchd/zhang40/ARM_data/sgp_cmip/'
    file_obs1=basedir1+'ARMdiag_domain_monthly_stat_cf.nc'
    file_obs2=basedir2+'ARMdiag_c1_monthly_stat_plev.nc'
    
    
    #modellist=['ACCESS1-0']
    #modellist=['CESM1-CAM5']
    modellist=['ACCESS1-0',
    'ACCESS1-3',
    'bcc-csm1-1-m',
    'bcc-csm1-1',
    'BNU-ESM',
    'CCSM4', #*clwvi for liquid only
    'CESM1-CAM5',#*
    #'CMCC-CM',
    #'CNRM-CM5',
    'CSIRO-Mk3-6-0', #*
    'CanAM4',
    #'EC-EARTH',
    'FGOALS-g2',
    'FGOALS-s2',
    #'GFDL-CM3',
    'GFDL-HIRAM-C360',
    'GFDL-HIRAM-C180',
    'GISS-E2-R',
    'HadGEM2-A',
    'inmcm4',
    'IPSL-CM5A-LR',  #*
    'IPSL-CM5A-MR',  #*
    'IPSL-CM5B-LR',  #*
    'MIROC5',
    'MPI-ESM-LR',   #*
    'MPI-ESM-MR',   #*
    'NorESM1-M']
    
    vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','ps','prw','cllvi','rsdscs','rldscs','albedo']#,'huss']
    xaxis=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Surface Pressure (Pa)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Downwelling clear-sky SW (W/m2)','Downwelling clear-sky LW (W/m2)','Surface Albedo']#,'Specific Humidity (kg/kg)']
    #vas=['tas']
    
    #va_ind=0
    xax =  np.arange (1,13,1)
    #ylim=[(-5,45),(0,6),(10,80),(20,90),(-10,140),(0,160),(300,550),(240,440),(10,80),(100,350),(-25,35),(5,45),(-0.1,0.25),(0,200),(0,200),(0.05,0.3)]
    pr_ac_mod=np.empty([len(modellist)+1,len(vas),12])*np.nan
    pr_ac_obs=np.empty([2, len(vas),12])*np.nan
    pr_ac_err=np.empty([2,len(modellist)+1,len(vas),12])*np.nan
    
    for va_ind in range(len(vas)):
    #    fig = plt.figure()# Create figure
    #    ax  =fig.add_axes([0.15, 0.15, 0.8, 0.8]) # Create axes
    #    colors = iter(cm.nipy_spectral(np.linspace(0, 1, len(modellist))))
        
        counter=0
        pr_yr_mmm= [0 for x in range(12)]
        pr_ac=np.empty([12])*np.nan
        for index in range(len(modellist)):
            print index+1,  modellist[index]
            if modellist[index] in ['GFDL-HIRAM-C180','GFDL-HIRAM-C360']:
                fin=cdms2.open(cmipdir+modellist[index]+'_amip_r2i1p1_mo_regrid_3x3_correct.nc')
            else:
                fin=cdms2.open(cmipdir+modellist[index]+'_amip_r1i1p1_mo_regrid_3x3_correct.nc')
            try:
                if va_ind == 0:
                    pr= fin('tas')
                    pr= [x -273.15 for x in pr]
                elif va_ind == 1:
                        pr =fin(vas[va_ind]) 
                        pr = [x *3600*24 for x in pr]
                elif va_ind == 12:
                     if modellist[index] in ['CCSM4','CESM1-CAM5','CSIRO-Mk3-6-0','IPSL-CM5A-LR','IPSL-CM5A-MR','IPSL-CM5B-LR','MPI-ESM-LR','MPI-ESM-MR']:
                         pr=fin('clwvi')
                         pr = [x *1 for x in pr]
                     else:
                         clwvi= fin('clwvi')
                         clivi= fin('clivi')
                         pr =[x - y for x, y in zip(clwvi, clivi)]
                elif va_ind == 15:
                    rsds= fin('rsds')
                    rsus= fin('rsus')
                    pr=[y/x for x,y in zip(rsds,rsus)]
                else:
                    pr =fin(vas[va_ind])
                    pr = [x *1 for x in pr]
                counter=counter+1
                pr_yr=np.reshape(pr,(len(pr)/12,12))
                pr_ac=np.nanmean(pr_yr,axis=0)
                pr_yr_mmm=pr_yr_mmm+pr_ac
            except:
                print 'Could not access variable ['+vas[va_ind]+'] from '+modellist[index]
                continue
    #        ax.plot(xax,pr_ac,'lightgrey',lw=1)
            pr_ac_mod[index,va_ind,:]=pr_ac
    #        ax.plot(xax,pr_ac,color=next(colors),label=modellist[index])
        if counter !=0:
            pr_yr_mmm=[x/(counter) for x in pr_yr_mmm]
        print '['+vas[va_ind]+'] retrived from ',counter, ' CMIP5 models'
        pr_ann=np.mean(pr_yr_mmm)
    #    ax.plot(xax,pr_yr_mmm,'k',label='MMM: %2.2f'%pr_ann,lw=3)
        pr_ac_mod[len(modellist),va_ind,:]=pr_yr_mmm
        
        np.savetxt(basedir+'cmip/'+vas[va_ind]+'_model_regrid_3x3_correct.csv',pr_ac_mod[:,va_ind,:],fmt='%.3f')
        #np.savetxt(basedir+'model/'+vas[va_ind]+'_'+modellist[index]+'_regrid_3x3_correct.csv',pr_ac_mod[0,va_ind,:],fmt='%.3f')
