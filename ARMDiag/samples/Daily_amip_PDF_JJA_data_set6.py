import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
import numpy as np

###################################Process Model data

filename=''
pr_model=np.empty([len(90*30])
pr_JJA_yr=np.empty([30,90])
print index+1,  modellist[index]
#fid_mod=cdms2.open(cmipdir+modellist[index]+'_amip_r1i1p1_da.nc')
fid_mod=cdms2.open(filename)
try:
  pr=fid_mod('pr')
except:
  print "Couldn't access variable"
  continue
pr = [x *3600 for x in pr[0:365*30]] #for pdf mm/hr 
for iy in range(30):
    pr_JJA_yr[iy,:]=pr[150+iy*365:240+iy*365] 

pr_model[:]=np.reshape(pr_JJA_yr,[90*30])
np.savetxt('data/pr_cmip_daily_JJA.csv',pr_model)

