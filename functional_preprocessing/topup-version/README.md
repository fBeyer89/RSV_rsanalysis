# LIFE_Lemon_mod_mod



# Results
The preprocessed resting state time series in MNI space can be found here:
resting_state -> ants -> rest_mni_unsmoothed.nii.gz
the same file with 6mm smoothing here:
resting_state -> FWHM6 -> rest_mni_smoothed.nii

## resting_state  
* ants  **EPI in MNI space**
    * rest_mni_unsmoothed_fullspectrum.nii.gz **preprocessed EPI in MNI space withouth BP filtering**  
    * rest_mni_unsmoothed.nii.gz  **preprocessed EPI in MNI space with BP filtering (0.01-0.1Hz)**  
* coregister  
    * rest2anat.dat.mincost **mincost file**  
    * rest_coregistered_nativespace.nii.gz  
    * rest_mean2anat_highres.nii.gz     **unwarped epi registered to anatomy**  
    * rest_mean2anat_lowres.nii.gz  
    * rest_mean2fmap.nii.gz  
    * rest_mean2fmap_unwarped.nii.gz  
    * T1_resampled.nii.gz  
    * transforms2anat  
        * B0_ph_fslprepared.nii.gz  
        * fullwarpfield.nii.gz  
        * rest2anat.dat  **transformation freesurfer format (fieldmap space to anatomy!)**    
        * rest2anat.mat  **transformation fsl format**  
* denoise  
    * artefact  **rapidart output files (outliers, outlier plot, global intensity, composite norm, stats)**
        * art.rest2anat_masked_outliers.txt  
        * global_intensity.rest2anat_masked.txt  
        * norm.rest2anat_masked.txt  
        * plot.rest2anat_masked.png  
        * stats.rest2anat_masked.txt  
    * mask  
        * T1_brain_mask2epi.nii.gz  **brain mask in original epi space (only for qa)**
        * T1_brain_mask_lowres.nii.gz  **brain mask used during artefact detection and 2nd glm**
        * wmcsf_mask_lowres.nii.gz  **white matter / csf mask used for acompcor**
    * regress **Nuisance Regression**
        * F_mcart.nii.gz  **F-values of full model fit 1st glm**
        * F_noise.nii.gz  **regressors 2nd glm**
        * mcart_regressor.txt   **regressors 1st glm**
        * noise_regressor.txt   **regressors 2nd glm**
        * pF_mcart.nii.gz  **p-values for full model fit 1st glm**
        * pF_noise.nii.gz  **F-values of full model fit 2nd glm**
    * rest_preprocessed_nativespace_fullspectrum.nii.gz **denoised EPI in native space withouth BP filtering**   
    * rest_preprocessed_nativespace.nii.gz  **denoised EPI in native space with BP filtering (0.01-0.1Hz) ** 
* FWHM6  
    * rest_mni_smoothed.nii.gz  **preprocessed EPI in MNI space with BP filtering (0.01-0.1Hz) and smoothing w 6mm**
* realign  
    * MAT                             **realignment matrices for all volumes**  
        * MAT_0000  
        * ....  
        * MAT_0294  
    * plots                           **plots of estimated motion**  
        * abs_displacement_plot.png  
        * rel_displacment_plot.png  
        * rotation_plot.png  
        * translation_plot.png  
    * rest_realigned_abs.rms          **absolute and relative rms displacement (similar to mean frame displacement)**  
    * rest_realigned_mean.nii.gz      **temporal mean after realignment**   
    * rest_realigned.par              **realignment parameters**  
    * rest_realigned_rel.rms          **absolute and relative rms displacement (similar to mean frame displacement)**  
    * rest_realigned_tsnr.nii.gz      **temporal snr after realignment**  


## structural  
* brain.nii.gz                        **skull stripped**  
* T1_brain2mni.nii.gz                 **brain in MNI152 1mm space**  
* T1_brain_mask.nii.gz                **brain mask**  
* T1.nii.gz                           **whole head after background masking in freesurfer space**  
* transforms2mni                      **transforms anatomy to MNI space (use antsApplyTransfom)**  
    * transform0GenericAffine.mat  
    * transform1InverseWarp.nii.gz    **inverse of nonlinear transformation**  
    * transform1Warp.nii.gz  
