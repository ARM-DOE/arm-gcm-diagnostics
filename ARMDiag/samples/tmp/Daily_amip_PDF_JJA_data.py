import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
from cdms2 import MV2
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


basedir='/p/lscratchd/zhang40/ARM_data/sgp.c1/'
cmipdir='/p/lscratchd/zhang40/ARM_data/sgp_cmip/'

file_obs=basedir+'monthly_atm_filled_sgp_inso.nc'
#file_obs=basedir+'monthly_cldrad_filled_sgp_inso.nc'
#modellist=['CCSM4']#,
modellist=['FGOALS-s2',
'IPSL-CM5A-LR',
'MPI-ESM-MR',
'bcc-csm1-1-m',
'IPSL-CM5A-LR',
'IPSL-CM5A-MR',
'IPSL-CM5B-LR',
'CSIRO-Mk3-6-0',
'MIROC5',
'ACCESS1-3',
'BNU-ESM',
'CMCC-CM',
'GFDL-CM3',
'ACCESS1-0',
'EC-EARTH',
'CCSM4',
'HadGEM2-A'
#'bcc-csm1-1_amip_r1i1p1_da.nc'
]

precip_cutoff=0.03  #mm/hr
######################Process ARMBE data
#print 'read data from : '
#print file_obs
#iyear=['1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009']
#iyear=map(str,range(1997,2012))
##print iyear
##iyear=['1994']
#pr_da=[]
#for index in range(len(iyear)):
#    print iyear[index],index
#    file_obs=basedir+'sgparmbeatmC1.c1.'+iyear[index]+'0101.000000.cdf'
##    file_obs=basedir+'sgparmbeatmC1.c1.19940101.000000.cdf'
#    fid_obs=cdms2.open(file_obs)
#    pr_obs=fid_obs('prec_sfc')
#    pr_hr=np.reshape(pr_obs,(len(pr_obs)/24,24))
#    #pr_hr= [x *24 for x in pr_hr] This way pr_hr is converted to a list
#    #pr_hr=24.0*np.array(pr_hr)
#    pr_da_yr=np.mean(pr_hr,axis=1)
#    pr_da_pre=pr_da_yr.data[np.where(pr_da_yr.data>precip_cutoff)]
#    pr_da.extend(pr_da_pre)
##    pr_da_compress=pr_da_yr.compress(pr_da_yr>=0)
##    pr_da.extend(pr_da_compress) 
#    fid_obs.close()
#
########################Process Continuous forcing data
#basedir='/p/lscratchd/zhang40/ARM_data/sgp.cf/'
##file_obs=basedir+'sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.19990101.000000.cdf'
##iname=['sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.','sgp60varanarucC1.c1.']
#iyr=['1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011']
##iyr=['1999']
#imon=['01','02','03','04','05','06','07','08','09','10','11','12']
#
#pr=np.empty([len(iyr)*365])
#pr_cf=[]
#for yr_ind in range(len(iyr)):
#    if iyr[yr_ind]=='1999' or iyr[yr_ind]=='2000' or iyr[yr_ind]=='2001':
#        iname='sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.'
#        precip='Prec'
#    else:
#        iname='sgp60varanarucC1.c1.'
#        precip='prec_srf'
#
#    pr_mon=[]
#    #for mon_ind in range(len(imon)):
#    for mon_ind in [5,6,7]:
#        file_obs=basedir+iname+iyr[yr_ind]+imon[mon_ind]+'01.000000.cdf'
#        print file_obs,iyr[yr_ind],imon[mon_ind]
#        try:
#            fid_obs=cdms2.open(file_obs)
#            pr_obs=fid_obs(precip) # mm/hr
#           # pr_1hr= np.mean(np.squeeze(pr_obs))
#            pr_1hr=np.squeeze(pr_obs)
##            pr_1hr=np.reshape(pr_1hr,(len(pr_1hr)/24,24))
##            pr_1hr=np.mean(pr_1hr,axis=1)
##            pr_1hr.shape
#            fid_obs.close()
#        except:
#            print "Couldn't access", file_obs
# #           pr_1hr=np.NaN
#            #When Continue is used here the NAN VALUE NOT WORK!
#        pr_cf.extend(pr_1hr)
#   # pr_yr.append(pr_mon)
#   # pr[yr_ind,:]=pr_mon
##pr_da1=pr_cf[0:365*13]
#pr_da1=pr_cf
#np.savetxt('data/pr_obs_daily_JJA.csv',pr_da1)
##pr_da1=np.reshape(pr_da1,(13,365))
##pr_da1=np.nanmean(pr_da1,axis=0)
##pr_da1=np.array(pr_cf)
#print 'pr_da1',pr_da1
##pr_da_cf=pr_da1[np.where(pr_da1>precip_cutoff)]
#pr_da_cf=pr_da1
###################################Process Model data

fig = plt.figure()# Create figure
#fig.set_size_inches(8,5)
ax  =fig.add_axes([0.12, 0.1, 0.85, 0.85]) # Create axes
xax =  np.arange (1,13,1)
#bins=[0.025+0.005*1.07**(x) for x in range(100)]
#bins=[0.001,0.01,0.1,0.5,1,2,5,10]
bins=[precip_cutoff,0.1,0.2,0.5,1,2,5,10]
tick_locs=[1,2,3,4,5,6,7]
tick_lbls=bins

mmm_pdf=np.empty([len(tick_locs)])
mmm_wday=0.0
counter=0
pr_model=np.empty([len(modellist),90*25])
pr_JJA_yr=np.empty([25,90])
for index in range(len(modellist)):
    print index+1,  modellist[index]
    fid_mod=cdms2.open(cmipdir+modellist[index]+'_amip_r1i1p1_da.nc')
    try:
      pr=fid_mod('pr')
    except:
      print "Couldn't access variable"
      continue
    pr = [x *3600 for x in pr[0:365*25]] #for pdf mm/hr 
    for iy in range(25):
        pr_JJA_yr[iy,:]=pr[150+iy*365:240+iy*365] 
        #pr_JJA_yr[iy,:]=pr[0+iy*365:365+iy*365] 
    
    pr_model[index,:]=np.reshape(pr_JJA_yr,[90*25])
    print pr_model
   # pr_mod=np.reshape(pr,(len(pr)/12,12))
   # pr_mo=np.mean(pr_mod,axis=0)
    #  ax.plot(xax,pr_mo)
    ind=np.where(np.squeeze(pr)>precip_cutoff)
  #  wday=100.0*np.size(ind)/np.size(np.squeeze(pr)>0)
    wday=100.0*np.size(ind)/np.size(np.squeeze(pr))
    mmm_wday=mmm_wday+wday
    pr=np.array(pr)
    print 'pr',pr.shape
    pr_wet=pr[np.where(pr>precip_cutoff)]
    mod=np.histogram(pr_wet,bins)
    mmm_pdf=mod[0]+mmm_pdf
    print 'mmm',mmm_pdf.shape
    counter=counter+1
pr_mmm=np.mean(pr_model,axis=0)

np.savetxt('data/pr_cmip_daily_JJA.csv',pr_model)
np.savetxt('data/pr_mmm_daily_JJA.csv',pr_mmm)
np.savetxt('data/pr_model_daily_JJA.csv',pr_model[0,:])
###########################Plotting

mmm_pdf_pct=[1.0*x/np.size(np.squeeze(pr))*100.0 for x in mmm_pdf]
h1=ax.bar(tick_locs,[x/counter for x in mmm_pdf_pct],width=0.1,color='b',align='center')
print h1
mmm_wday=mmm_wday/counter
ax.text(0.8, 0.7,'MMM wet'+'%.2f' % mmm_wday,color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)

#obs1=np.histogram(pr_da,bins)
#num_day_obs1=1.0*len(iyear)*365
#obs1_pct=[x/num_day_obs1*100.0 for x in obs1[0]]
#ax.bar([x-0.2 for x in tick_locs],obs1_pct,width=0.1,color='b',align='center')
#wday_ob=np.size(pr_da)/num_day_obs1*100
#ax.text(0.8, 0.9,'ARMBE wet'+'%.2f' % wday_ob,color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
#
obs2=np.histogram(pr_da_cf,bins)
num_day_obs2=np.size(pr_da1)
obs2_pct=[1.0*x/num_day_obs2*100.0 for x in obs2[0]]
print obs2,obs2_pct,num_day_obs2
ax.bar([x-0.1 for x in tick_locs],obs2_pct,width=0.1,color='k',align='center')
wday_ob=100.0*np.size(pr_da_cf)/num_day_obs2
ax.text(0.8, 0.8,'OBS wet'+'%.2f' % wday_ob,color='k',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)

num_day_mod=np.size(np.squeeze(pr))
mod_pct=[1.0*x/num_day_mod*100.0 for x in mod[0]]
ax.bar([x+0.1 for x in tick_locs],mod_pct,width=0.1,color='r',align='center')
# plt.gca().set_xscale("log")
ax.text(0.8, 0.6,'MOD wet'+'%.2f' % wday,color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)

tick_locs=[0.5,1.5,2.5,3.5,4.5,5.5,6.5]
plt.xticks(tick_locs,tick_lbls)

plt.title('Precip daily mean PDF: SGP')
plt.xlabel('Precipitation rate (mm/hr)')
plt.ylabel('Frequency')
#for the minor ticks, use no labels; default NullFormatter
#plt.legend([OBS,MMM],('OBS','MMM'),loc=0)
#fig.savefig("figures/Daily_pdf_pr.ps")#, dpi=200,bbox_inches='tight')
#plt.show()

