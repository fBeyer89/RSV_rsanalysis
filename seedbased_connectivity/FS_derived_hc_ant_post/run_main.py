# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:27:06 2015

@author: fbeyer
"""

from main import create_hc_connec
import sys
import os
'''
Meta script to run lemon resting state preprocessing
---------------------------------------------------
Can run in two modes:
python run_lemon_resting.py s {subject_id}
python run_lemon_resting.py f {text file containing list of subjects}
'''
mode=sys.argv[1]
if mode == 's':
    subjects=[sys.argv[2]]
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        subjects = [line.strip() for line in f]

side="right" #CHANGE IN HC.py so that correct FS side is selected!!!
for subject in subjects:
    print 'Running subject '+subject
    working_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/wd/hipp_connectivity_thr099/' + side + '/' +subject+'/'
    #os.makedirs(working_dir)
    data_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/'+subject+'/'
    #os.makedirs(data_dir)

    freesurfer_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/freesurfer'
    
    resting_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/preprocessed/'+subject
    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    standard_brain_resampled = '/home/raid1/fbeyer/Documents/Scripts/ICA_RSN_analysis/MNI/MNI_resampled.nii'
    standard_brain_mask = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'
    standard_brain_mask_resampled='/home/raid1/fbeyer/Documents/Scripts/ICA_RSN_analysis/MNI/MNI_resampled_brain_mask.nii.gz'
    #os.makedirs(resting_dir)
    #os.makedirs(data_dir)
    epi_resolution = 2.0
    fwhm_smoothing = 6.0
    create_hc_connec(subject=subject, working_dir=working_dir, data_dir=data_dir,
                  freesurfer_dir=freesurfer_dir, 
                  out_dir=resting_dir, epi_resolution=epi_resolution, 
                  standard_brain = standard_brain,
                  standard_brain_resampled = standard_brain_resampled, 
                  standard_brain_mask = standard_brain_mask,
                  standard_brain_mask_resampled = standard_brain_mask_resampled,
                  fwhm_smoothing = fwhm_smoothing, side=side)
    
    
