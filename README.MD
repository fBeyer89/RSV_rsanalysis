# preprocessing of 3T resting-state data from RESVERATROL-Study (NRO-148)

* functional_preprocessing: nipype-based scripts for resting-state preprocessing (see README in folder for more details)
* quality_reports: nipype-based scripts for quality control
	- quality_reports/julia_qa/ -> quality reports based on Julia Huntenburgs scripts (**generate_report_part2.py**)
	- quality_reports/poldrack_qa -> quality reports based on Russ Poldrack (**QA_and_header_fix_wf.py**)
	- compare_meanFD/ -> comparison of mean FD estimated by two pipelines (detection of error related to angle/radians in calculation of FD)
	- hippocampal_subfields/ -> quality control of hippocampus connectivity (**generate_report.py**)

* seedbased_connectivity: nipype-based scripts to generate hippocampus connectivity
	- after_scrubbing_FS_derived_hc_ant_post (seed based connectivity based on Freesurfer ROIs & scrubbed data)
	- SCA (seed based connectivity absed on MNI coordinates)
	- FS_derived_hc_ant_post (seed based connectivity based on Freesurfer ROIs)
	- transform_HC_to_MNI (transform HC maps to MNI space for quality control)

* import_from_afs.sh (get data from AFS repository)

