def normalization_fullspectrum(subject, working_dir, data_dir, freesurfer_dir, out_dir,
                       vol_to_remove, TR, epi_resolution, highpass, lowpass,
                       echo_space, te_diff, pe_dir, standard_brain, standard_brain_resampled, standard_brain_mask,
                       standard_brain_mask_resampled, fwhm_smoothing):
    from nipype.pipeline.engine import Node, Workflow
    import nipype.interfaces.io as nio
    import nipype.interfaces.fsl as fsl
    from ants_registration import create_ants_registration_pipeline

    fsl.FSLCommand.set_default_output_type('NIFTI_GZ')
    # main workflow
    func_preproc = Workflow(name='lemon_resting')
    func_preproc.base_dir = working_dir
    func_preproc.config['execution']['crashdump_dir'] = func_preproc.base_dir + "/crash_files"
    # select files
    templates = {
        'ts_fullspectrum': 'Lemon_mod/{subject_id}/lemon_resting/denoise/filternoise/rest2anat_denoised.nii.gz',
        # 'func': 'func/EPI_t2.nii',
        # 'fmap_phase': 'unwarp/B0_ph.nii',
        # 'fmap_mag': 'unwarp/B0_mag.nii',
        # 'anat_head': 'preprocessed/mod/anat/T1.nii.gz',  # either with mod or without
        # 'anat_brain': 'preprocessed/mod/anat/brain.nii.gz',
        # # new version with brain_extraction from freesurfer  #T1_brain_brain.nii.gz',
        # 'brain_mask': 'preprocessed/mod/anat/T1_brain_mask.nii.gz',  # T1_brain_brain_mask.nii.gz',
        'ants_affine': 'subjects/{subject_id}/preprocessed/mod/anat/transforms2mni/transform0GenericAffine.mat',
        'ants_warp': 'subjects/{subject_id}/preprocessed/mod/anat/transforms2mni/transform1Warp.nii.gz'
        }
    # base = /scr/kennedy2/data_fbeyer/genetics/
    selectfiles = Node(nio.SelectFiles(templates,
                                       base_directory=data_dir),
                       name="selectfiles")
    selectfiles.inputs.subject_id = subject



    # FL added fullspectrum
    # workflow to transform fullspectrum timeseries to MNI
    ants_registration_full = create_ants_registration_pipeline('ants_registration_full')
    ants_registration_full.inputs.inputnode.ref = standard_brain_resampled

    # FL added fullspectrum
    func_preproc.connect(selectfiles, 'ts_fullspectrum', ants_registration_full, 'inputnode.denoised_ts')
    func_preproc.connect(selectfiles, 'ants_affine', ants_registration_full, 'inputnode.ants_affine')
    func_preproc.connect(selectfiles, 'ants_warp', ants_registration_full, 'inputnode.ants_warp')


    # sink to store files
    sink = Node(nio.DataSink(parameterization=False,
                             base_directory=out_dir,
                             substitutions=[
                                 # ('fmap_phase_fslprepared', 'fieldmap'),
                                 # ('fieldmap_fslprepared_fieldmap_unmasked_vsm', 'shiftmap'),
                                 # ('plot.rest_coregistered', 'outlier_plot'),
                                 # ('filter_motion_comp_norm_compcor_art_dmotion', 'nuissance_matrix'),
                                 # ('rest_realigned.nii.gz_abs.rms', 'rest_realigned_abs.rms'),
                                 # ('rest_realigned.nii.gz.par', 'rest_realigned.par'),
                                 # ('rest_realigned.nii.gz_rel.rms', 'rest_realigned_rel.rms'),
                                 # ('rest_realigned.nii.gz_abs_disp', 'abs_displacement_plot'),
                                 # ('rest_realigned.nii.gz_rel_disp', 'rel_displacment_plot'),
                                 # ('art.rest_coregistered_outliers', 'outliers'),
                                 # ('global_intensity.rest_coregistered', 'global_intensity'),
                                 # ('norm.rest_coregistered', 'composite_norm'),
                                 # ('stats.rest_coregistered', 'stats'),
                                 # ('rest_denoised_bandpassed_norm.nii.gz',
                                 #  'rest_preprocessed_nativespace.nii.gz'),
                                 # ('rest_denoised_bandpassed_norm_trans.nii.gz',
                                 #  'rest_mni_unsmoothed.nii.gz'),
                                 # ('rest_denoised_bandpassed_norm_trans_smooth.nii',
                                 #  'rest_mni_smoothed.nii'),
                                 # FL added
                                 ('rest2anat_denoised.nii.gz', 'rest_preprocessed_nativespace_fullspectrum.nii.gz'),
                                 ('rest2anat_denoised_trans.nii.gz', 'rest_mni_unsmoothed_fullspectrum.nii.gz')
                             ]),
                name='sink')

    func_preproc.connect(ants_registration_full, 'outputnode.ants_reg_ts', sink, 'ants.@antsnormalized_fullspectrum')


    func_preproc.write_graph(dotfilename='func_preproc.dot', graph2use='colored', format='pdf', simple_form=True)
    func_preproc.run(plugin='CondorDAGMan')
    #func_preproc.run()
