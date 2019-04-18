# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:27:06 2015

@author: fbeyer
run:
python functional/run_lemon_resting_sample5.py f /scr/kennedy2/liem/subjects_lists/subjects_big_sample5_2_clean_n1184.txt
"""

from functional.lemon_resting import create_lemon_resting
import sys
import os

'''
Meta script to run lemon resting state preprocessing
---------------------------------------------------
Can run in two modes:
python run_lemon_resting.py s {subject_id}
python run_lemon_resting.py f {text file containing list of subjects}
'''
mode = sys.argv[1]
if mode == 's':
    subjects = [sys.argv[2]]
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        subjects = [line.strip() for line in f]

for subject in subjects:
    print 'Running subject ' + subject
    ##
    root_dir = '/scr/kennedy2/liem/sample_5'
    # working_dir = os.path.join(root_dir, 'wd', subject)
    # working_dir = os.path.join('/scr/kansas1/liem/sample_5', 'wd', subject)
    working_dir = os.path.join('/nobackup/clustercache/liem/sample_5', 'wd', subject)

    data_dir = os.path.join(root_dir, 'subjects', subject)
    out_dir = os.path.join(data_dir, 'preprocessed/mod/resting/')

    freesurfer_dir = '/scr/kennedy2/LIFE/freesurfer_all/'

    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    standard_brain_mask = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

    standard_brain_resampled = '/scr/kennedy2/liem/Templates/MNI_resampled.nii'
    standard_brain_mask_resampled = '/scr/kennedy2/liem/Templates/MNI_resampled_brain_mask.nii'

    echo_space = 0.000512  # in sec
    te_diff = 2.46  # in ms
    epi_resolution = 3.0
    TR = 2.0
    highpass = 0.01
    lowpass = 0.1
    vol_to_remove = 5
    pe_dir = 'y-'
    fwhm_smoothing = 6.0
    create_lemon_resting(subject=subject,
                         working_dir=working_dir,
                         data_dir=data_dir,
                         freesurfer_dir=freesurfer_dir,
                         out_dir=out_dir,
                         vol_to_remove=vol_to_remove,
                         TR=TR,
                         epi_resolution=epi_resolution,
                         highpass=highpass,
                         lowpass=lowpass,
                         echo_space=echo_space,
                         te_diff=te_diff,
                         pe_dir=pe_dir,
                         standard_brain=standard_brain,
                         standard_brain_resampled=standard_brain_resampled,
                         standard_brain_mask=standard_brain_mask,
                         standard_brain_mask_resampled=standard_brain_mask_resampled,
                         fwhm_smoothing=fwhm_smoothing)
