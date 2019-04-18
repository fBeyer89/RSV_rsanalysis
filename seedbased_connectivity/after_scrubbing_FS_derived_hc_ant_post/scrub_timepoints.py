# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:18:25 2017

@author: fbeyer
"""

def scrub_timepoints(scrubvols, in_file, working_dir):
    import numpy as np
    import nibabel as nb
    import os

    scrubvols=np.loadtxt(scrubvols)
    print "%s working dir" %working_dir
    print 'loading in-file'
    img = nb.load(in_file)
    imgdata = img.get_data()
    
    scrubbed_vol=np.delete(imgdata,scrubvols,axis=3)

    scrubbed_vol_img = nb.Nifti1Image(scrubbed_vol, img.get_affine())
    
    print "finished calculating"
    filename= os.path.join(working_dir,'hc_connec_thr099_scrubbed/scrub_volumes/scrubbed_vol.nii.gz')
    nb.save(scrubbed_vol_img,filename)

    
    return filename
    

