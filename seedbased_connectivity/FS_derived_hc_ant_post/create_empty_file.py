# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:35:51 2017

@author: fbeyer
"""

def scrub_vols(infile, cog):

    import numpy as np
    import nibabel as nb
    import os, sys
    from time import sleep


    print('#####################')
    print('#####################')
    print('#####################')

            #load 4d nifti image
    nifti = nb.load(infile)
    img = nb.Nifti1Image(nifti.get_data()[:, :, :, :], nifti.get_affine())
    print(img.header['pixdim'][4])
    #img.header['pixdim'][4] = 1.4
    #print(img.header['pixdim'][4])
   
    hc_roi=img.dataobj[:,:,cog:256]
    anterior_fill=img.dataobj[:,:,0:cog]
    anterior_hc=np.concatenate((anterior_fill, hc_roi),axis=2)
    
    hc_roi=img.dataobj[:,:,0:cog]
    posterior_fill=img.dataobj[:,:,cog:256]
    posterior_hc=np.concatenate((hc_roi, posterior_fill),axis=2)


    anterior_hc_img = nb.Nifti1Image(anterior_hc, img.get_affine())
    posterior_hc_img = nb.Nifti1Image(posterior_hc, img.get_affine())

    tmp = scan + '.feat/'
    anterior_img_out_file = os.path.join(data_dir, subject, 'preprocessed/functional', tmp, 'anterior_roi.nii.gz')
    posterior_img_out_file = os.path.join(data_dir, subject, 'preprocessed/functional', tmp, 'anterior_roi.nii.gz')
    # assign ts to out_file
    anterior_hc_img.to_filename(anterior_img_out_file)
    posterior_hc_img.to_filename(posterior_img_out_file)

    return anterior_img_out_file, posterior_img_out_file

