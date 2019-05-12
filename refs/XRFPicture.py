import fabio
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
mpl.rcParams.update({'font.size':18,'axes.titlesize':14})

beam_dir='/asap3/petra3/gpfs/external/2018/data/50000209/scratch_cc/Summytest/CIGS/CIGS_Run10Summed3eleMatrix/'
sample_dir='CIGS_smallgrain'

Run= 10
Size=124
x_step=0.04
y_step=0.04





def loadelement(El,Line):
    return fabio.open(beam_dir+'IMAGES/'+sample_dir+'_sum3_'+str(Run).zfill(4)+'_0000_0000_to_'+str(Size).zfill(4)+'_'+El+'_'+Line+'.edf')


def saveimage(im,cmap,xlab,ylab,clab,fil,name):
    plt.figure() 
    plt.imshow(im.data,interpolation=fil, cmap=cmap, alpha=1., extent=[0,x_size*x_step,0,y_size*y_step],origin='upper')
    plt.subplots_adjust(bottom=0.2)
    plt.xticks([0, 1 ,2 ,3 ,4],('0', '1', '2', '3', '4'))
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    cbar =plt.colorbar()
    cbar.ax.set_ylabel(clab)
    plt.savefig(name)
    plt.close()
    
In=loadelement('In','L')
Cu=loadelement('Cu','K')
y_size,x_size = np.shape(Cu.data)
print(np.shape(Cu.data))
saveimage(Cu,'viridis','X Position (µm)','Y Position (µm)','Concentration (a.u.)','None','Cu_Ka'+str(Run)+'sum.png')
saveimage(In,'viridis','X Position (µm)','Y Position (µm)','Concentration (a.u.)','None','In_L'+str(Run)+'sum.png')
