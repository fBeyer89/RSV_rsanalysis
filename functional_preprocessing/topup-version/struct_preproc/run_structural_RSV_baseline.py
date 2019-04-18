# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:10:25 2015

@author: fbeyer
run:
python struct_preproc/run_structural_RSV_baseline.py 

"""

from structural import create_structural
import sys, os

'''
Meta script to run structural preprocessing
------------------------------------------
Can run in two modes:
python run_structural.py s {subject_id}
python run_structural.py f {text file containing list of subjects}
'''
mode = sys.argv[1]

if mode == 's':
    subjects = [sys.argv[2]]
    print subjects
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        subjects = [line.strip() for line in f]

# select fold
# subjects = subjects[:1300]
#subjects = subjects[1300:]


for subject in subjects:
    print 'Running subject ' + subject
    root_dir = '/data/p_nro148/probands_mri_blood/'#'/a/projects/nro148_resveratrol/probands/'
    #root_dir_2 = '/data/liem-2/LIFE'
    root_dir2 = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/'
    working_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/wd/'+subject#os.path.join(root_dir2, 'wd', subject)
    data_dir = os.path.join(root_dir, subject)
    out_dir = os.path.join(root_dir2, 'preprocessed', subject, 'structural')

    freesurfer_dir = '/data/pt_nro148/3T/restingstate_and_freesurfer/preprocessing/freesurfer/'

    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    create_structural(subject=subject, working_dir=working_dir, data_dir=data_dir,
                      freesurfer_dir=freesurfer_dir, out_dir=out_dir,
                      standard_brain=standard_brain)
