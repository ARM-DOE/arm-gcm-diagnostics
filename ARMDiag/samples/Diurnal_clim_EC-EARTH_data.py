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
#cl_ob=ma.mean(pr_2d,axis=1)
#cl_p=ma.mean(pr1_2d,axis=1)
#cl_ob_diurnal=ma.mean(pr_2d,axis=0)
#cl_p_diurnal=ma.mean(pr1_2d,axis=0)
#cl_ob_ann=ma.mean(cl_ob,axis=0)
#cl_p_ann=ma.mean(cl_p,axis=0)
#####################Monthly Mean Diurnal Cycle
#
#for index in range(2):
#    fig1, axs = plt.subplots(4,3, figsize=(15, 12), facecolor='w', edgecolor='k',sharex=True,sharey=True)
#    fig1.subplots_adjust(hspace = .3, wspace=.1)
#    axs = axs.ravel()
#    month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#    for imon in range(12):
#        if index==0:
#             title='ARSCL_cl_mon_diurnal_clim'
#             yy=np.linspace(0,23,24)
#             xx=np.linspace(100,1000,37)
#             x,y=np.meshgrid(xx,yy)
#             pr_2d_con=np.concatenate((pr_2d[imon,:,:],pr_2d[imon,:,:]),axis=0)#6 hour GMT to Local time
#             im=axs[imon].pcolormesh(y,x,pr_2d_con[6:30,::-1], vmin=0, vmax=25)
#             plt.xlim([0,23])
#             xax =  np.arange (0,24,3)
#             my_xticks = ['0','3','6','9','12','15','18','21']
#   
#        else:
#             title='CFMIP2_EC-EARTH_cl_mon_diurnal_clim'
#             yy=np.linspace(0,7,8)
#             xx=np.linspace(100,1000,37)
#             x,y=np.meshgrid(xx,yy)
#             pr_2d_con=np.concatenate((pr1_2d[imon,:,:],pr1_2d[imon,:,:]),axis=0)
#             #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
#             im=axs[imon].pcolormesh(y,x,pr_2d_con[1:9,::-1], vmin=0, vmax=25)
#             plt.xlim([0,7])
#             xax =  np.arange (0,8,1)
#             my_xticks = ['0','3','6','9','12','15','18','21']
#
#        axs[imon].set_title(month[imon])
#        plt.xticks(xax, my_xticks)
#        plt.setp(axs[imon].get_xticklabels(), visible=True)
#    for ax in axs[9:12]:
#        ax.set_xlabel('Local time (hr)')
#    for ax in axs[::3]:
#        ax.set_ylabel('Pressure (mb)')
#    axs[0].invert_yaxis()
#    plt.suptitle(title)
#    fig1.subplots_adjust(right=0.8)
#    cbar_ax = fig1.add_axes([0.85, 0.15, 0.05, 0.7])
#    fig1.colorbar(im, cax=cbar_ax)
#    plt.title('cl (%)')
#    fig1.savefig('figures/'+title+'.png')
#    plt.show()
#
###########################Diurnal cycle
#
#for index in range(2):
#    fig2 = plt.figure()# Create figure
#    ax  =fig2.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
#    if index==0:
#         title='ARSCL_cl_diurnal_clim'
#         yy=np.linspace(0,23,24)
#         xx=np.linspace(100,1000,37)
#         x,y=np.meshgrid(xx,yy)
#         pr_2d_con=np.concatenate((cl_ob_diurnal,cl_ob_diurnal),axis=0)#6 hour GMT to Local time
#         im=ax.pcolormesh(y,x,pr_2d_con[6:30,::-1], vmin=0, vmax=25)
#         plt.xlim([0,23])
#         xax =  np.arange (0,24,3)
#         my_xticks = ['0','3','6','9','12','15','18','21']
#
#    else:
#         title='CFMIP2_EC-EARTH_cl_diurnal_clim'
#         yy=np.linspace(0,7,8)
#         xx=np.linspace(100,1000,37)
#         x,y=np.meshgrid(xx,yy)
#         pr_2d_con=np.concatenate((cl_p_diurnal,cl_p_diurnal),axis=0)
#         #Starting time is 3:00:00 GTM, +3 hour GMT to Local time
#         im=ax.pcolormesh(y,x,pr_2d_con[1:9,::-1], vmin=0, vmax=25)
#         plt.xlim([0,7])
#         xax =  np.arange (0,8,1)
#         my_xticks = ['0','3','6','9','12','15','18','21']
#
#    plt.xticks(xax, my_xticks)
#    plt.ylabel('Pressure (mb)')
#    plt.xlabel('Local time (hr)')
#    plt.gca().invert_yaxis()
#    plt.suptitle(title)
#    cbar_ax = fig2.add_axes([0.85, 0.15, 0.05, 0.75])
#    fig2.colorbar(im, cax=cbar_ax)
#    plt.title('cl (%)')
#    fig2.savefig('figures/'+title+'.png')
##    
#    plt.show()
###########################Annual cycle
#
#yy=np.linspace(0,11,12)
#xx=np.linspace(100,1000,37)
#x,y=np.meshgrid(xx,yy)
#for index in range(3):
#    fig = plt.figure()# Create figure
#    ax  =fig.add_axes([0.15, 0.15, 0.65, 0.75]) # Create axes
#    if index==0:
#        title='ARSCL_cl_annual_cycle_clim'
#        im=ax.pcolormesh(y,x,cl_p.data[:,::-1], vmin=0, vmax=25)
#    elif index==1:
#        im=ax.pcolormesh(y,x,cl_ob.data[:,::-1], vmin=0, vmax=25)
#        title='CFMIP2_EC-EARTH_cl_annual_cycle_clim'
#    elif index==2:
#        im=ax.pcolormesh(y,x,cl_p.data[:,::-1]-cl_ob.data[:,::-1], vmin=-10, vmax=10)
#        title='Diff_cl_annual_cycle_clim'
#    xax =  np.arange (0,12,1)
#    my_xticks = ['J','F','M','A','M','J','J','A','S','O','N','D']
#    plt.xticks(xax, my_xticks)
#    plt.xlim(0,11)
#    plt.ylabel('Pressure (mb)')
#    plt.gca().invert_yaxis()
#    plt.suptitle(title)
#    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.75])
#    fig.colorbar(im, cax=cbar_ax)
#    plt.title('cl (%)')
#    fig.savefig('figures/'+title+'.png')
##    
#    plt.show()
#    
############################Seasonal Mean
#levels=xx
#seasons=['MAM','JJA','SON','DJF']
#cl_p2=np.concatenate((cl_p,cl_p),axis=0)
#cl_ob2=np.concatenate((cl_ob,cl_ob),axis=0)
#for index in range(len(seasons)):
#   
#    print index*3+2,(index+1)*3+2
#    fig3 = plt.figure()# Create figure
#    ax  =fig3.add_axes([0.15, 0.1, 0.8, 0.8]) # Create axes
#    ax.plot(np.mean(cl_p2.data[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'r',lw=3,label='EC-EARTH')
#    ax.plot(np.mean(cl_ob2.data[index*3+2:(index+1)*3+2,::-1],axis=0),levels,'k',lw=3,label='OBS')
#    plt.gca().invert_yaxis()
#    plt.ylabel('Pressure (mb)')
#    plt.xlabel('Cloud fraction (%)')
#    plt.xlim([0,25])
#    plt.legend(loc='best',prop={'size':15})
#    plt.title(seasons[index]+' Mean Cloud Fraction')
#    fig3.savefig('figures/'+seasons[index]+'_ARSCL_CFMIP2_EC-EARTH.png')
#    plt.show()
#
#
#
#fig0 = plt.figure()# Create figure
#ax  =fig0.add_axes([0.15, 0.1, 0.8, 0.8]) # Create axes
#ax.plot(cl_p_ann.data[::-1],levels,'r',lw=3,label='EC-EARTH')
#ax.plot(cl_ob_ann.data[::-1],levels,'k',lw=3,label='OBS')
#plt.gca().invert_yaxis()
#plt.ylabel('Pressure (mb)')
#plt.xlabel('Cloud fraction (%)')
#plt.xlim([0,25])
#plt.legend(loc='best',prop={'size':15})
#plt.title('Annual Mean Cloud Fraction')
#fig0.savefig('figures/Annual_ARSCL_CFMIP2_EC-EARTH.png')
#plt.show()
