# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:35:51 2017

@author: fbeyer
"""

def create_anterior_posterior_hippocampus(in_file, cog, working_dir, subject_id):

    import numpy as np
    import nibabel as nb
    import os, sys
    from time import sleep


    print('#####################')
    print('#####################')
    print('#####################')
    print working_dir
            #load 4d nifti image
    nifti = nb.load(in_file)
    img = nb.Nifti1Image(nifti.get_data()[:, :, :], nifti.get_affine())
    #img.header['pixdim'][4] = 1.4
    #print(img.header['pixdim'][4])
   
    print np.shape(img.dataobj)
    hc_roi=img.dataobj[:,:,cog:256]
    anterior_fill=img.dataobj[:,:,0:cog]*0
    anterior_hc=np.concatenate((anterior_fill, hc_roi),axis=2)
    anterior_hc_img = nb.Nifti1Image(anterior_hc, img.get_affine())
    out_file = working_dir + '/hc_connec_thr099/transform_hc/anterior_hc.nii.gz' #os.path.join(data_dir, subject, 'preprocessed/functional', tmp, )
    print out_file    
    anterior_hc_img.to_filename(out_file)
    
    hc_roi=img.dataobj[:,:,0:cog]
    posterior_fill=img.dataobj[:,:,cog:256]*0
    posterior_hc=np.concatenate((hc_roi, posterior_fill),axis=2)
    posterior_hc_img = nb.Nifti1Image(posterior_hc, img.get_affine())
    out_file = working_dir + '/hc_connec_thr099/transform_hc/posterior_hc.nii.gz'
    print out_file   
    
    posterior_hc_img.to_filename(out_file)
    
    return True #nonsense output as it doesn't work anyway



    
    

