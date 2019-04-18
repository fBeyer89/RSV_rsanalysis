# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:27:06 2015

@author: fbeyer
run:
python functional/run_lemon_resting_LIFE16.py f /scr/adenauer2/Franz/LIFE16/LIFE16_subjects_list_n2557.txt
"""

from lemon_resting import create_lemon_resting
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


# select fold
# subjects = subjects[:450]
#subjects = subjects[450:900]
#subjects = subjects[612:900]
#subjects = subjects[713:900]
#subjects = subjects[900:1400]
#subjects = subjects[1058:1400]
#subjects = subjects[1152:1400]
#subjects = subjects[1309:1400]
# subjects = subjects[1152:1309]
# subjects = subjects[1400:1900]
# subjects = subjects[1900:]
#subjects = subjects[2097:]
#subjects = subjects[2353:]
# subjects = subjects[2357:]

for subject in subjects:
    print 'Running subject ' + subject
    
    root_dir = '/scr/aventurin3/RSV/3T/rs/'
    root_dir_2 = '/scr/aventurin3/RSV/3T/rs/wdr/' #'/data/liem-2/LIFE'
    working_dir = os.path.join(root_dir_2, 'wd', subject)
    data_dir = root_dir
    out_dir = os.path.join(root_dir, 'preprocessed', subject, 'resting_state')

    freesurfer_dir = '/scr/aventurin3/RSV/3T/freesurfer/'

    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    standard_brain_mask = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain_mask.nii.gz'

    standard_brain_resampled = '/scr/adenauer2/Franz/LIFE16/Templates/MNI_resampled.nii'
    standard_brain_mask_resampled = '/scr/adenauer2/Franz/LIFE16/Templates/MNI_resampled_brain_mask.nii'

    echo_space = 0.00063 
    #see: https://lcni.uoregon.edu/kb-articles/kb-0003    
    #Effective Echo Spacing (s) = 1/(BandwidthPerPixelPhaseEncode * MatrixSizePhase) = 0.63ms
    #in /home/raid1/fbeyer/Documents/Scripts/rs_preprocessing/RSV/topup-version/aquisition_params_RSV.txt
    #--> Total readout time (FSL) = (number of echoes - 1) * echo spacing = (88-1)*0.63ms=54.81 ms
    epi_resolution = 2.0 #??
    TR = 1.4
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
                         pe_dir=pe_dir,
                         standard_brain=standard_brain,
                         standard_brain_resampled=standard_brain_resampled,
                         standard_brain_mask=standard_brain_mask,
                         standard_brain_mask_resampled=standard_brain_mask_resampled,
                         fwhm_smoothing=fwhm_smoothing)
