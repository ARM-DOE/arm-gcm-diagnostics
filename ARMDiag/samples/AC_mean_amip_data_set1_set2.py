import os,sys
import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
import matplotlib.pyplot as plt
import numpy as np

"""Sample code to process data into the csv form, generating mean annual cycle from monthly mean """
    
#Put in the directory and model output file
filename=''

#Available model variables, name convention follows CMIP5 standard output (http://cmip-pcmdi.llnl.gov/cmip5/data_description.html)
vas=['tas','pr','clt','hurs','hfss','hfls','rlus','rlds','rsus','rsds','ps','prw','cllvi','rsdscs','rldscs','albedo']
xaxis=['Surface Temperature (C)','Precipitation (mm/day)','Total Cloud Fraction (%)','Rel. Humidity (%)','Sensible Heat Flux (W/m2)','Latent Heat Flux(W/m2)','Upwelling LW (W/m2)','Downwelling LW (W/m2)','Upwelling SW (W/m2)','Downwelling SW (W/m2)','Surface Pressure (Pa)', 'Preciptable Water (mm)', 'Liquid Water Path (mm)','Downwelling clear-sky SW (W/m2)','Downwelling clear-sky LW (W/m2)','Surface Albedo']

pr_ac_mod=np.empty([len(vas),12])*np.nan

for va_ind in range(len(vas)):
    
    counter=0
    pr_ac=np.empty([12])*np.nan
    fin=cdms2.open(filename)
    try:
        if va_ind == 0:
            pr= fin('tas')
            pr= [x -273.15 for x in pr]
        elif va_ind == 1:
                pr =fin(vas[va_ind]) 
                pr = [x *3600*24 for x in pr]
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
        print 'Could not access variable ['+vas[va_ind]+'] from model'
        continue
    pr_ac_mod[va_ind,:]=pr_ac

#Place the processed data under ARMDiag/model
    np.savetxt(basedir+'model/'+vas[va_ind]+'_model_regrid_3x3_correct.csv',pr_ac_mod[va_ind,:],fmt='%.6f')
