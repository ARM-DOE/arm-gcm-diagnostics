import cdms2, MV2, regrid,vcs, cdutil, genutil, os, sys,math
from cdms2 import MV2
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure, show, rc, grid
import numpy as np
import matplotlib.cm as cm
from scipy.optimize import curve_fit

#basedir='/scratch/zhang40/ARM_data/sgp.c1/'
#cmipdir='/scratch/zhang40/ARM_data/sgp_cmip/'
basedir='/p/lscratchd/zhang40/ARM_data/sgp.c1/'
cmipdir='/p/lscratchd/zhang40/ARM_data/sgp_cmip/'

#file_obs=basedir+'diurnal_atm_filled_sgp_inso.nc'
file_obs=basedir+'diurnal_atm_filled_sgp_inso.nc'
f_in=cdms2.open(file_obs)
pr=f_in('prec_sfc')
pr_july=np.array(pr[:,6,:])
pr_july=np.mean(pr_july,axis=1)
####################Process ARMBE 
#iyear=['1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009']
##iyear=['1994','1995']
#pr_obs7=np.empty([len(iyear),720])
#for index in range(len(iyear)):
#    print iyear[index],index
#    file_obs=basedir+'sgparmbeatmC1.c1.'+iyear[index]+'0101.000000.cdf'
##    file_obs=basedir+'sgparmbeatmC1.c1.19940101.000000.cdf'
#    fid_obs=cdms2.open(file_obs)
#    pr_obs=fid_obs('prec_sfc',time=(iyear[index]+'-07-01',iyear[index]+'-07-31'))
#    pr_obs7[index,:]=pr_obs
#pr_obs7mean=np.mean(pr_obs7,axis=0)
#pr_obsday=pr_obs7mean.reshape(30,24)
#pr_obsday=np.mean(pr_obsday,axis=0)
##ydata= [0.21075041592121124  ,0.2516006827354431  ,0.22898930311203003
##          , 0.2289973348379135  ,0.14670906960964203 ,0.15586285293102264
##          , 0.14696434140205383 ,0.11742854118347168 ,0.1280999779701233
##          , 0.07390599697828293 ,0.07402268052101135 ,0.08369521051645279
##          , 0.0780443623661995  ,0.057751238346099854, 0.09882914274930954
##          , 0.09057489782571793 ,0.06787288933992386 ,0.0846576988697052
##          , 0.12092535942792892 ,0.2048588991165161  ,0.1352657526731491
##          , 0.06342179328203201 ,0.10273883491754532 ,0.22715681791305542]
##ydata=[ 0.32157502,  0.26386178,  0.20754856,  0.13463148,  0.12056711,
##        0.15563385,  0.21345907,  0.10488449,  0.10265833,  0.053975  ,
##        0.03204398,  0.02922176,  0.06984584,  0.03825535,  0.11373493,
##        0.08815417,  0.04725876,  0.08967888,  0.1539363 ,  0.29460379,
##        0.09029939,  0.0197069 ,  0.02355834,  0.29707882]

##############################Process Continuous Forcing
#basedir='/p/lscratchd/zhang40/ARM_data/sgp.cf/'
##file_obs=basedir+'sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.19990101.000000.cdf'
##iname=['sgp1hrRUCbasedV2.0_ConstrVarAna_X1.c1.','sgp60varanarucC1.c1.']
#iyr=['1999','2000','2001','2002','2003','2004','2005','2006','2007','2008']#,'2009','2010','2011']
##iyr=['2002']
#imon=['01','02','03','04','05','06','07','08','09','10','11','12']
#
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
#    mon_ind='06'   #For July
#    file_obs=basedir+iname+iyr[yr_ind]+'0601.000000.cdf'
#    print file_obs,iyr[yr_ind]
#    try:
#        fid_obs=cdms2.open(file_obs)
#        pr_obs=fid_obs(precip) # mm/hr
#        pr_1hr=np.squeeze(pr_obs)
#        #pr_1hr=np.reshape(pr_1hr,(31,24))
#        pr_1hr=np.reshape(pr_1hr,(30,24))
#       # pr_1hr=np.mean(pr_1hr,axis=1)
#        pr_1hr.shape
#        print pr_1hr.shape
#        fid_obs.close()
#    except:
#        print "Couldn't access", file_obs
##        pr_1hr=np.NaN
#        #When Continue is used here the NAN VALUE NOT WORK!
#    pr_cf.extend(pr_1hr)
#pr_cf_1hr=np.nanmean(np.array(pr_cf),axis=0)
#print pr_cf_1hr

#############################Fitting
ydata=[ 0.32157502,  0.26386178,  0.20754856,  0.13463148,  0.12056711,
        0.15563385,  0.21345907,  0.10488449,  0.10265833,  0.053975  ,
        0.03204398,  0.02922176,  0.06984584,  0.03825535,  0.11373493,
        0.08815417,  0.04725876,  0.08967888,  0.1539363 ,  0.29460379,
        0.09029939,  0.0197069 ,  0.02355834,  0.29707882]
ydata_cf_7 =[ 0.09697157,  0.10176183,  0.10359112,  0.1063955 ,  0.10953732,  0.11769301,
  0.13103129,  0.14920329,  0.16784067,  0.1780723 ,  0.17700896,  0.15996319,
  0.13550013,  0.10893973,  0.08505762,  0.06545085,  0.05049372,  0.04226376,
  0.03886204,  0.04108336,  0.04892029,  0.06100653,  0.07483919,  0.08682867]
ydata_cf_6=[ 0.17637143,  0.19765013 , 0.21463598 , 0.23162015 , 0.25347888,  0.27872238,
  0.2999039  , 0.31409511,  0.32006207,  0.31787705,  0.3033556 ,  0.2858389,
  0.26724356 , 0.24665517,  0.2194678 ,  0.19091782,  0.16628695,  0.14995621,
  0.13703802 , 0.13160384,  0.13004385,  0.13556686,  0.14495073,  0.16068067]
ydata_cf_5=[ 0.13698104 , 0.1551491  , 0.17738397 , 0.20039666 , 0.2286341  , 0.2456319,
  0.25300136 , 0.2543166 ,  0.2586455 ,  0.25863817,  0.24708383,  0.22075665,
  0.19222511 , 0.16563086,  0.14316429,  0.12001719,  0.10043233,  0.08637581,
  0.08485549 , 0.09229093,  0.10337701,  0.10954732,  0.11097617,  0.11267158]
ydata_cf_4=[ 0.11491682, 0.11666131,  0.11813286,  0.11826467,  0.11322781 , 0.10616725,
  0.09924037 , 0.09995838,  0.10736719,  0.11186898,  0.10617741,  0.09339388,
  0.08218358 , 0.07480115,  0.07238442,  0.07394601,  0.08020316,  0.08557672,
  0.08996671 , 0.09349882,  0.10314213,  0.11586776,  0.12670435,  0.12652762]

ydata_cf=[ydata_cf_4[i]+ydata_cf_5[i]+ydata_cf_6[i]+ydata_cf_7[i]for i in range(len(ydata_cf_4))]
ydata_cf=[x /4.0 for x in ydata_cf]

modellist=['MIROC5','CMCC-CM','inmcm4','CCSM4','GFDL-HIRAM-C180','GFDL-HIRAM-C360','FGOALS-g2','EC-EARTH','ACCESS1-0','ACCESS1-3','bcc-csm1-1-m','IPSL-CM5A-LR']
pr_cmip=np.empty([len(modellist)+3,8])
mod_phase=np.empty([len(modellist)+3])
mod_amp=np.empty([len(modellist)+3])

#JULY
#0 MIROC5
pr_cmip[0,:]=[ 0.92302471 , 0.28017925 , 0.31932922 , 0.29208408 , 0.36739762 , 1.31146073 ,  2.64319792,  2.40768653]
#1 CMCC-CM
pr_cmip[1,:]=[ 1.881078   , 0.53731652 , 0.57092305 , 0.46087582 , 0.99900144 , 1.01479478,  2.33608438,  3.46167094]
#2 inmcm4
pr_cmip[2,:]=[ 0.2721111  , 0.35155555 , 0.50544443 , 0.61722221 , 0.73966665 , 0.67522221,0.82666665,  0.59688888]
#3 CCSM4
pr_cmip[3,:]=[ 2.56443525 , 1.16827066 , 0.81021995 , 0.69690534 , 0.73593132 , 1.13757948,3.37185181,  3.98623778]
#4 GFDL-HIRAM-C180
pr_cmip[4,:]=[ 0.2667631  , 0.49606445 , 1.15721806 , 1.10173755 , 0.52976051 , 0.75538711,1.6914904 ,  0.77893813]
#5 GFDL-HIRAM-C360
pr_cmip[5,:]=[ 0.43224573 , 0.76287032 , 0.50017684 , 0.25984453 , 0.48877035 , 0.5434558,0.80097683 , 0.63205966]
#6 FGOALS-g2
pr_cmip[6,:]=[ 1.67942407 , 1.72797846 , 1.52303697 , 1.73105104 , 1.62495632 , 1.1973538,1.24386348 , 1.55712567]
#7 EC-EARTH
pr_cmip[7,:]=[ 0.40966261 , 0.42910739 , 0.65695243 , 0.82486551 , 1.13401781 , 3.03732942,2.72566164,  1.06543012]
#8 ACCESS1-0
pr_cmip[8,:]=[ 0.92481872 , 0.98045539 , 1.09877559 , 1.45485003 , 1.50408898 , 1.45165914,  1.28779956,  0.77151133]
#9 ACCESS1-3
pr_cmip[9,:]=[ 1.06334041 , 1.21065211 , 1.19726788 , 1.52492202 , 1.48796198 , 1.85201925, 2.29676513 , 1.48680525]
#10 bcc-csm1-1-m
pr_cmip[10,:]=[ 0.67272005,  0.6942546 ,  0.9173066 ,  1.025667  ,  0.90104061,  0.72330995, 0.8125742 ,  0.72905349]
#11 IPSL-CM5A-LR
pr_cmip[11,:]=[ 0.03265279,  0.04333767,  0.07459295,  0.13235548,  0.30590355,  3.10697027, 3.39178515,  0.61858753]
#modellist=['MIROC5']
#0 ACME_amip_CNTL
pr_cmip[12,:]=[ 3.03659738 , 1.77790315 , 1.03571037 , 0.96840491 , 0.9162352 ,  1.09778075, 2.26983642 , 3.43132413]
#1 ACME_amip_CLUBBE
pr_cmip[13,:]=[ 1.90469501 , 1.61564595 , 1.18130542 , 0.80192817 , 0.63896305,  0.5974121 , 1.25630124 , 1.85919777]
#2 ACME_amip_UNICON
pr_cmip[14,:]=[ 5.17212135 , 3.88506211 , 1.84319267 , 1.05227703 , 0.61830958,  0.3742670 , 0.77974283 , 2.88682523]

ydata_cf=ydata_cf_7

#JUne
#pr_cmip[0,:]=[ 1.27087111,  0.35393397 , 0.45386778 , 0.63834943 , 1.19294082 , 2.29854466,3.91419865,  3.44148732]
#pr_cmip[1,:]=[ 3.41811999,  1.57219627 , 1.43303091 , 2.17404986 , 2.1995183  , 2.72380536, 4.77325021,  6.1214761 ]
#pr_cmip[2,:]=[ 1.15494251,  0.77494251 , 0.96528733 , 1.23999997 , 1.34666664 , 1.65528733,2.21172408,  2.01333329]
#pr_cmip[3,:]=[ 4.73638134,  3.389201   , 2.6399495  , 2.33490553 , 2.23283376 , 2.52206332,5.54273312,  6.58447951]
#pr_cmip[4,:]=[ 0.61644289,  1.50282908 , 2.16026437 , 2.54001209 , 3.0117671  , 2.79154556, 3.54771901,  2.04187516]
#pr_cmip[5,:]=[ 1.63937319,  0.87848122 , 1.93402817 , 2.44089848 , 2.37799418 , 1.92916768,  2.06004894,  1.0685459 ]
#pr_cmip[6,:]=[ 1.63540525,  1.63934709 , 1.65959532 , 1.67623329 , 1.45657314 , 0.97287747,  0.96498742,  1.38434392]
#pr_cmip[7,:]=[ 1.54742657,  1.55040938 , 1.5441708  , 1.89653764 , 2.41898798 , 4.5568871,  4.20732095,  2.18562128]
#pr_cmip[8,:]=[ 1.35914092,  1.78176181 , 2.49347332 , 2.95681374 , 2.9626669  , 3.42673122,  3.26187525,  1.58388092]
#pr_cmip[9,:]=[ 1.65988835,  1.96696542 , 2.17112778 , 1.95359387 , 2.06568359 , 3.46900864,  4.17178356,  2.58895632]
#pr_cmip[10,:]=[ 0.87218286,  1.20205146 , 1.70993455 , 1.69740961 , 1.56492499 , 1.40457528,  1.34991204,  1.12948496]
#pr_cmip[11,:]=[ 0.06315381,  0.10607472 , 0.19250943 , 0.32500831 , 0.36483804 , 1.74614008,  2.59444189,  0.57055377]
#
##ACME
#pr_cmip[12,:]=[ 3.80982769,  3.12844625 , 1.9805535 ,  1.29842901 , 1.50934988 , 2.36404641,
#  3.90208833,  4.2004569 ]
#pr_cmip[13,:]=[ 5.05820558,  4.08055767 , 2.4799511 ,  1.76012825 , 1.58063239 , 1.98150552,
#  3.72363729,  5.24001009]
#pr_cmip[14,:]=[ 2.62616365,  2.57859996 , 1.22905926,  0.67579285 , 0.22016273 , 0.22082007,
#  0.45189625,  1.26644425]
#
#ydata_cf=ydata_cf_6
##pr_cmip[12,:]=[ 3.81504373 , 2.87392757,  1.92247792,  1.60347563,  1.65109404,  1.95572959,  3.06002662,  3.80062491]
##pr_cmip[13,:]=[ 3.49866159 , 3.23229229,  2.48580893,  2.22673466,  1.9345241 ,  1.86038118,  2.79199971,  3.59507128]
##pr_cmip[14,:]=[ 2.94584818 , 2.61445261,  1.378176  ,  0.90096724,  0.76386   ,  0.63709949,  0.78769767,  1.7525942 ]







fig0 = plt.figure()
ax0=fig0.add_axes([0.14, 0.14, 0.84, 0.84])
xax_3r=np.array([3.0*x-6.5 for x in range(8)])
xax_cf=np.array([1.0*x-6.5 for x in range(24)])  #convert from GMT to LST -6.5 form SGP
colors = iter(cm.rainbow(np.linspace(0, 1, 12)))
for mod in range(len(modellist)+3):
    pr_day=pr_cmip[mod,:]

    def func24(x, p1,p2):
      return p1*np.sin(2*np.pi/24*x+p2)

    popt, pcov = curve_fit(func24, xax_3r, pr_day,p0=(1.0,0.2))
    p1_mod = popt[0]
    p2_mod = popt[1]
#    print 'aaa', p1_mod,p2_mod

    ymod_fit=func24(xax_cf,p1_mod,p2_mod)+np.mean(pr_day)
    if mod<12 :
#        if p1_mod >0:
            mod_fit,=ax0.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ymod_fit,ymod_fit)), 'lightgrey',lw=1)
##            mod_fit,=ax0.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ymod_fit,ymod_fit)), color=next(colors),lw=2)
    if mod == 12:
       mod_fit,=ax0.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ymod_fit,ymod_fit)),'r', label = 'MOD',lw=2)
       ax0.plot(np.concatenate((xax_3r,[x+24 for x in xax_3r])),np.concatenate((pr_day,pr_day)),'.r',label='MOD',lw=2,markersize=15)
       print np.concatenate((xax_3r,[x for x in xax_3r])),np.concatenate((pr_day,pr_day))

    mod_amp[mod]=p1_mod
    #treatment for phase: If p1 smaller than 0 then curve is cosine
#    if p1_mod<=0:
#       mod_phase[mod]=0.5*np.pi-p2_mod+np.pi#-6.5/24*2*np.pi
#    if p1_mod>0:
#       mod_phase[mod]=p2_mod+0.5*np.pi#-6.5/24*2*np.pi
#
    if p1_mod<=0 :
       p2_mod=1.5*np.pi-p2_mod
    if p1_mod>0 :
       p2_mod=0.5*np.pi-p2_mod
      # print p1_mod,p2_mod,mod
    mod_phase[mod]=p2_mod

#    arr2=pr_day-np.mean(pr_day)
#    sp=np.fft.fft(arr2)
#    ps=np.abs(sp)
#    freqs=np.fft.fftfreq(arr2.size,3)
#    ind=np.where((ps==np.max(ps)))
#    #print 'fft',ind, freqs[ind],np.max(ps),np.angle(sp[ind]) ,np.abs(sp[ind])
#    angle=abs(np.angle(sp[ind]))#-5.0/2/np.pi+1.5*np.pi
#    amp=np.abs(sp[ind])/len(arr2)
#    fft_amp=amp*2.0
#    fft_phase=-angle-6.5/24*2*np.pi
#    mod_phase[mod]=fft_phase[0]
#    mod_amp[mod]=fft_amp[0]
#    print 'angle',np.angle(sp[ind],deg=True),fft_amp,fft_phase
#    print 'fft,phase,amp',mod, mod_phase[mod],mod_amp[mod]
#    print '-------------------------------'


    #print mod_phase[mod],mod_amp[mod],p2_mod,p1_mod




xax=np.array([1.0*x for x in range(24)])
def func24(x, p1,p2):
  return p1*np.sin(2*np.pi/24*x+p2)


ydata_cf=[x*24.0 for x in ydata_cf]
popt, pcov = curve_fit(func24, xax_cf, ydata_cf,p0=(1.0,0.2))
p1_cf = popt[0]
p2_cf = popt[1]
obs2,=plt.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])),np.concatenate((ydata_cf,ydata_cf)),'k.',label='OBS',lw=2,markersize=15)
yobs2=func24(xax_cf,p1_cf,p2_cf)+np.mean(ydata_cf)
obs_fit2,=plt.plot(np.concatenate((xax_cf,[x+24 for x in xax_cf])), np.concatenate((yobs2,yobs2)),'k',lw=2)

my_xticks=['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h']
my_xticks_loc=np.array([3*x for x in range(8)])
plt.xticks(my_xticks_loc, my_xticks)
ax0.set_xlim([0,24])
ax0.set_ylim([-0.5,10])
ax0.set_ylim([-0.5,7])
#plt.legend(handles=[obs2,mod_fit],loc='upper center')
#ax1.set_xticklabels(['19h', '22h', '1h', '4h', '7h', '10h', '13h', '16h'])
ax0.text(0.3, 0.95,'OBS',color='k',verticalalignment='top', horizontalalignment='left',transform=ax0.transAxes)
ax0.text(0.3, 0.85,'MOD',color='r',verticalalignment='top', horizontalalignment='left',transform=ax0.transAxes)
plt.xlabel('local solar time [hr]')
plt.ylabel('precipitation at surface [mm/day]')
plt.show()

#
#
#######################################Map phase and amplitude to Dial
#obs_amp=abs(p1)
#obs_phase=0.5*np.pi-p2  #-5.0/24*2*np.pi
obs2_amp=abs(p1_cf)
obs2_phase=0.5*np.pi-p2_cf  #-5.0/24*2*np.pi
#mod_amp=abs(p1_mod)
#mod_phase=0.5*np.pi-p2_mod#-6.5/24*2*np.pi
#
#
#arr2=pr_7mean-np.mean(pr_7mean)
#sp=np.fft.fft(arr2)
#ps=np.abs(sp)
#freqs=np.fft.fftfreq(arr2.size,3)
#ind=np.where((ps==np.max(ps)))
#print 'fft',ind, freqs[ind],np.max(ps),np.angle(sp[ind]) ,np.abs(sp[ind])
#angle=abs(np.angle(sp[ind]))#-5.0/2/np.pi+1.5*np.pi
#amp=np.abs(sp[ind])/len(arr2)
#
#fft_amp=amp*2.0
#fft_phase=-angle-6.5/24*2*np.pi
#print np.angle(sp[ind],deg=True),fft_amp,fft_phase
###################Create Harmonic Dial Figure
fig2 = plt.figure()
ax2  =fig2.add_axes([0.1, 0.1, 0.8, 0.8],polar=True)#, axisbg='#d5de9c')

size=50
#ax2.scatter(obs_phase,obs_amp,color='b',label='ARMBE',s=size)
ax2.scatter(obs2_phase,obs2_amp,color='k',label='OBS',s=size*2)
print 'check',mod_phase[14],mod_amp[14]
ax2.scatter(mod_phase[0:11],abs(mod_amp[0:11]),color='lightgrey',s=size)
#for ind in range(12):
##    if mod_amp[ind] >0 :
#        ax2.scatter(mod_phase[ind],abs(mod_amp[ind]),s=size,color='lightgrey')#marker=next(markers),label=ind)
ax2.scatter(mod_phase[12],abs(mod_amp[12]),color='r',label='MOD',s=size*2)
##ax2.scatter(fft_phase,fft_amp,color='b',label='fft')
#r = np.arange(0, obs_amp, 0.05)
#r2 = np.arange(0, obs2_amp, 0.05)
#theta = r*0.0+obs_phase
#theta2 = r2*0.0+obs2_phase
#ax2.plot(theta,r,color='b')
#ax2.plot(theta2,r2,color='k')
ax2.legend(scatterpoints=1,loc='center right',bbox_to_anchor=(1.2,0.90),prop={'size':15})
#ax2.scatter(p2-5.0/24*2*np.pi-0.5*np.pi,obs_amp)
#ax2.scatter(0,obs_amp)
#arr=plt.arrow(0,0,obs_phase,obs_amp)
ax2.set_rmax(3)
ax2.set_theta_direction(-1)
ax2.set_theta_offset(np.pi/2)
ax2.set_xticklabels(['0h', '3h', '6h', '9h', '12h', '15h', '18h', '21h'])
grid(True)

#ax2.set_title("Mapping 1st Harmonic", fontsize=15)
#fig0.savefig("figures/Diurnal_ACME_07_For_Steve_v1.eps")
fig0.savefig("figures/DC_amip_07_pr.png")
fig2.savefig("figures/DC_amip_HarmonicD_07_pr.png")
#fig1.savefig("figures/Diurnal_Cycle_pr_July.ps")
#fig2.savefig("figures/Diurnal_Harmonicycle_ACME_07_ForGleckler.eps")
plt.show()




