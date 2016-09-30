from matplotlib.pyplot import grid
import matplotlib.pyplot as plt
import numpy as np
import os,sys
import config

def Daily_amip_PDF_plot():
    mod = config.modelname
    pathname = os.path.dirname(sys.argv[0])
    basedir=os.path.abspath(pathname)+'/ARMDiag/'
    vas=['pr']
    for va_ind in range(len(vas)):
        pr_obs=np.loadtxt(basedir+'observation/'+vas[va_ind]+'_JJA_daily_obs.csv')
        pr_cmip=np.loadtxt(basedir+'cmip/'+vas[va_ind]+'_JJA_daily_model_regrid_3x3_correct.csv')
        pr_mod=np.loadtxt(basedir+'model/'+vas[va_ind]+'_JJA_daily_'+mod+'_regrid_3x3_correct.csv')
        
        precip_cutoff=0.03-0.0025/2  #mm/hr
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
        
        
        bins_width=[0.0025*1.2**(x) for x in range(55)]
        bins=accum(bins_width)
        bins=[x for x in bins]
        
        ######################Use same method to calculate PDFs for obs, model and cmip multi-models.
        for index in range(pr_cmip.shape[0]+1):
            if index==0:
               pr_da_cf=[x*24.0 for x in pr_obs]
            elif index==1:
               pr_da_cf=[x*24.0 for x in pr_mod]
            else:
               pr_da_cf=[x*24.0 for x in pr_cmip[index-2,:]]
        
            pr_da_cf=np.array(pr_da_cf)
            ind=np.where(pr_da_cf>precip_cutoff)
            pr_da=pr_da_cf[ind]
            y,binEdges=np.histogram(pr_da,bins=bins,density=True)
            cumulative = np.cumsum(y*(binEdges[1:]-binEdges[:-1]))
            wday_ob=100.0*np.size(pr_da)/np.size(pr_da_cf)
        
            if index==0 :
                ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'r',lw=3)
                y1=y*0.5*(binEdges[1:]+binEdges[:-1])
                ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'r',lw=3)
            elif index==1 :
                ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'b',lw=3)
                y1=y*0.5*(binEdges[1:]+binEdges[:-1])
                ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'b',lw=3)
        
            else :
                ax.plot(0.5*(binEdges[1:]+binEdges[:-1]),y,'grey',lw=1)
                y1=y*0.5*(binEdges[1:]+binEdges[:-1])
                ax1.plot(0.5*(binEdges[1:]+binEdges[:-1]),y1,'grey',lw=1)
                cumulative1 = np.cumsum(y1*(binEdges[1:]-binEdges[:-1]))
            ax.text(0.85, 0.9,'OBS',color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
            ax.text(0.85, 0.8,'MOD',color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
            ax1.text(1.2, 1,'OBS',color='r',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
            ax1.text(1.2, 0.9,'MOD',color='b',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes)
        
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlim([0.05,200])
            ax.set_ylim([0.0001,20])
            ax.set_ylabel('Frequency')
            ax.set_xlabel('Precipitation rate (mm/day)')
            ax1.set_xlim([0.05,200])
            ax1.set_ylim([0.01,1])
            ax1.set_xscale('log')
            ax1.set_yscale('log')
            ax1.set_ylabel('Precipitation Amount (mm/day)')
            ax1.set_xlabel('Precipitation rate (mm/day)')
            fig.savefig(basedir+'figures/Daily_amip_'+vas[va_ind]+'_JJA_pdf1.png')
            fig1.savefig(basedir+'figures/Daily_amip_'+vas[va_ind]+'_JJA_pdf2.png')
