# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:10:46 2017

@author: fbeyer
"""


#textfile1='/home/raid1/fbeyer/Documents/Scripts/RSV_scripts/3Tpreprocessing/seedbased_connectivity/cog.txt'

def load_prep_cog(textfile):
    "rounds the y-coordinate of the center-of-gravity and calculates other useful numbers"
    import numpy as np
  
    cogfile=np.loadtxt(textfile)
    print cogfile
    y_coord=cogfile[2]    #because the file is still in FS-orientation where the third dimension is y
    y_coord_rounded=np.round(y_coord)
    print y_coord_rounded
    
    #total voxels in y dimension are 256 (like in other 2 dimensions)
    #0 is defined at the posterior edge of the brain, 256 is at the anterior end
    dim_y_anterior=256-y_coord_rounded #goes from the slice of the center of gravity to 256
    dim_y_posterior=y_coord_rounded #goes from 0 to one slice before the center of gravity
    print "%d until %d = anterior (size=%d)" %(y_coord_rounded, 255, dim_y_anterior)
    print "%d until %d = posterior (size=%d)" %(0, dim_y_posterior, y_coord_rounded)
    
    
    #output the start of the anterior with its size and the start of the posterior = 0 with its size
    #the start of the 
    return int(y_coord_rounded), int(dim_y_anterior), int(dim_y_posterior) 
    
#load_prep_cog(textfile1)