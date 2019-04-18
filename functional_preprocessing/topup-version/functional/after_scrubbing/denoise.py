# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:34:01 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Node, Workflow, MapNode
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.utility as util
import nipype.algorithms.rapidart as ra
import nipype.interfaces.afni as afni
#from motreg import motion_regressors, calc_friston_twenty_four
#from motionfilter import build_filter1
#from compcor import extract_noise_components
from normalize_timeseries import time_normalizer
#from nipype.utils.filemanip import list_to_filename
#from fix_header_tr import fix_TR_fs

'''
Main workflow for denoising
Largely based on https://github.com/nipy/nipype/blob/master/examples/
rsfmri_vol_surface_preprocessing_nipy.py#L261
but denoising in anatomical space
'''


def create_denoise_pipeline(name='denoise'):
    # workflow
    denoise = Workflow(name='denoise')
    # Define nodes
    inputnode = Node(interface=util.IdentityInterface(fields=['anat_brain',
                                                              'brain_mask',
                                                              'epi_denoised',
                                                              'highpass_sigma',
                                                              'lowpass_sigma',
                                                              'tr']),
                     name='inputnode')
    outputnode = Node(interface=util.IdentityInterface(fields=[# FL added fullspectrum
                                                               'normalized_file']),
                      name='outputnode')
    

    # bandpass filter denoised file
    bandpass_filter = Node(fsl.TemporalFilter(out_file='rest_denoised_bandpassed.nii.gz'),
                           name='bandpass_filter')
    bandpass_filter.plugin_args = {'submit_specs': 'request_memory = 17000'}
    denoise.connect([(inputnode, bandpass_filter, [('highpass_sigma', 'highpass_sigma'),
                                                   ('lowpass_sigma', 'lowpass_sigma')]),
                     # (filter2, bandpass_filter, [('out_res', 'in_file')]),
                     # (filter2, outputnode, [('out_res', 'ts_fullspectrum')]),
                     (inputnode, bandpass_filter, [('epi_denoised', 'in_file')])
                     ])
    # time-normalize scans
    normalize_time = Node(util.Function(input_names=['in_file', 'tr'],
                                        output_names=['out_file'],
                                        function=time_normalizer),
                          name='normalize_time')
    normalize_time.plugin_args = {'submit_specs': 'request_memory = 17000'}
    denoise.connect([(inputnode, normalize_time, [('tr', 'tr')]),
                     (bandpass_filter, normalize_time, [('out_file', 'in_file')]),
                     (normalize_time, outputnode, [('out_file', 'normalized_file')])
                     ])
    return denoise
