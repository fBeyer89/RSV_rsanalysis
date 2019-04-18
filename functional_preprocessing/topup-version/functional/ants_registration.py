# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 14:00:12 2015

@author: fbeyer
"""
from nipype.pipeline.engine import MapNode, Node, Workflow
import nipype.interfaces.utility as util
import nipype.interfaces.fsl as fsl
import nipype.interfaces.ants as ants
from fix_header_tr import fix_TR_fs


def create_ants_registration_pipeline(name='ants_registration'):
    # set fsl output type
    fsl.FSLCommand.set_default_output_type('NIFTI_GZ')
    # initiate workflow
    ants_registration = Workflow(name=name)
    # inputnode
    inputnode = Node(util.IdentityInterface(fields=['denoised_ts',
                                                    'ants_affine',
                                                    'ants_warp',
                                                    'ref',
                                                    'tr_sec'
                                                    ]),
                     name='inputnode')
    # outputnode
    outputnode = Node(util.IdentityInterface(fields=['ants_reg_ts',
                                                     ]),
                      name='outputnode')

    # also transform to mni space
    collect_transforms = Node(interface=util.Merge(2), name='collect_transforms')

    ants_reg = Node(ants.ApplyTransforms(input_image_type=3, dimension=3, interpolation='Linear'), name='ants_reg')

    # ants does something strange with headers. TR seems to be preserved (nibabel, fslinfo) but mri_info does not
    # display correct TR
    fix_tr = Node(util.Function(input_names=['in_file', 'TR_sec'], output_names=['out_file'], function=fix_TR_fs),
                  name='fix_tr')
    ants_registration.connect(inputnode, 'tr_sec', fix_tr, 'TR_sec')
    ants_registration.connect(ants_reg, 'output_image', fix_tr, 'in_file')

    ants_registration.connect([
        (inputnode, ants_reg, [('denoised_ts', 'input_image')]),
        (inputnode, ants_reg, [('ref', 'reference_image')]),
        (inputnode, collect_transforms, [('ants_affine', 'in1')]),
        (inputnode, collect_transforms, [('ants_warp', 'in2')]),
        (collect_transforms, ants_reg, [('out', 'transforms')]),
        #(ants_reg, outputnode, [('output_image', 'ants_reg_ts')])
        (fix_tr, outputnode, [('out_file', 'ants_reg_ts')])
    ])

    return ants_registration
