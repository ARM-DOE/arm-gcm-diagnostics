import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import math


basedir='/g/g92/zhang40/calc_stats'
pr_mod=genfromtxt(basedir+'/data/pr'+'_model_daily_JJA.csv')
pr_cmip=genfromtxt(basedir+'/data/pr'+'_cmip_daily_JJA.csv')
pr_obs=genfromtxt(basedir+'/data/pr'+'_obs_daily_JJA.csv')
#pr_cmip=genfromtxt(basedir+'/data/pr'+'_cmip_daily.csv')
print pr_cmip.shape

precip_cutoff=0.03-0.0025/2  #mm/hr
#precip_cutoff=-2  #mm/hr
#######################Process Continuous forcing data
#pr_da_cf=pr_obs
##################################Process Model data

fig = plt.figure()# Create figure
ax  =fig.add_axes([0.15, 0.15, 0.8, 0.8]) # Create axes
xax =  np.arange (1,13,1)

fig1 = plt.figure()# Create figure
ax1  =fig1.add_axes([0.15, 0.15, 0.8, 0.8]) # Create axes
def accum(list):
    """Sequential accumulation of the original list"""
    result = []
    for i in range(len(list)):
        result.append(sum(list[:i+1]))
    return result


#bins_width=[0.0025*1.07**(x) for x in range(146)]
#bins_width=[0.0025*1.1**(x) for x in range(100)]
bins_width=[0.0025*1.2**(x) for x in range(55)]
bins=accum(bins_width)
#bins=[x+0.0275 for x in bins]
#bins=[np.log(x) for x in bins]
bins=[x for x in bins]
#print bins

for index in range(pr_cmip.shape[0]):
    if index==0:
       pr_da_cf=[x*24.0 for x in pr_obs]
    else:
       pr_da_cf=[x*24.0 for x in pr_cmip[index-1,:]]

    pr_da_cf=np.array(pr_da_cf)
    ind=np.where(pr_da_cf>precip_cutoff)
    pr_da=pr_da_cf[ind]
#    print np.mean(pr_da_cf),np.mean(pr_da)
    y,binEdges=np.histogram(pr_da,bins=bins,density=True)
#    y= [1.0*x/np.size(pr_da) for x in y]
#    y=1.0*y/np.size(pr_da)
    cumulative = np.cumsum(y*(binEdges[1:]-binEdges[:-1]))
    wday_ob=100.0*np.size(pr_da)/np.size(pr_da_cf)
    
    print np.size(pr_da),np.size(pr_da_cf),wday_ob
    if index==0 :
        ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'r',lw=3)
        y1=y*0.5*(binEdges[1:]+binEdges[:-1])
        ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'r',lw=3)
    elif index==11 :
        ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'b',lw=3)
        y1=y*0.5*(binEdges[1:]+binEdges[:-1])
        ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'b',lw=3)
        
    else :
        ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'lightgrey',lw=1)
        y1=y*0.5*(binEdges[1:]+binEdges[:-1])
        ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'lightgrey',lw=1)
        cumulative1 = np.cumsum(y1*(binEdges[1:]-binEdges[:-1]))
    ax.text(0.85, 0.9,'OBS',color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
    ax.text(0.85, 0.8,'MOD',color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
    ax1.text(1.2, 1,'OBS',color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
    ax1.text(1.2, 0.9,'MOD',color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
      
#print pr_da.shape
#plt.plot(bins[0:len(bins)-1],obs2[0])
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim([0.05,200])
    ax.set_ylim([0.0001,20])
    #ax.set_ylim([0.001,200])
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Precipitation rate (mm/day)')
#    ax.set_title('JJA Precip PDF: SGP') 
    ax1.set_xlim([0.05,200])
    ax1.set_ylim([0.01,1])
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_ylabel('Precipitation Amount (mm/day)')
    ax1.set_xlabel('Precipitation rate (mm/day)')
#    ax1.set_title('JJA Precip PDF: SGP') 
#    plt.title('JJA Precip PDF: SGP')
#for the minor ticks, use no labels; default NullFormatter
#plt.legend([OBS,MMM],('OBS','MMM'),loc=0)
fig.savefig("figures/Daily_pdf_pr_JJA_frequency.png")#, dpi=200,bbox_inches='tight')
fig1.savefig("figures/Daily_pdf_pr_JJA_amount.png")#, dpi=200,bbox_inches='tight')
plt.show()

