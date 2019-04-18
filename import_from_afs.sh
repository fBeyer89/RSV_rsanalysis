#!/bin/bash

#usage: ./x0_preprocess [subListFile]
#create folder structure and copy the data from the RSV-study-folder to the subject's folders

orig_dir="/data/p_nro148/probands_mri_blood/"
results_dir="/data/pt_nro148/3T/restingstate_and_freesurfer/raw/"

#subj_file="/data/pt_nro148/3T/restingstate_and_freesurfer/Lists/RSV_3T_FU_all_available_subjects_RSV152_163.txt"
#"/scr/aventurin3/data_fbeyer/RSV/3T/preprocessing/Lists/RSV_3T_Baseline_subjects_nifti_25.7.txt" 

read_files()
{
#while read DEM
#do 

#subject="${DEM}"
#
for subject in RSV143 RSV150
do
echo "-----------------------------------"
echo "processing $subject"
echo "-----------------------------------"

#create folders for checking and data
mkdir -p $results_dir/$subject/check
mkdir -p $results_dir/$subject/func
mkdir -p $results_dir/$subject/anat
mkdir -p $results_dir/$subject/topup


#copy the first in the list of MPRAGE-images found.. (supposingly they are all the same)
first_dir=$orig_dir/$subject/3T/nifti/
echo $first_dir
#set -- $first_dir
#echo "$1" >> $results_dir/$subject/check/images_used.txt

#copy the first in the list of anatomical images
anat_name=$(find $first_dir -name oMPRAGEADNI32Ch* | sort) 
echo $anat_name
anat_arr=($anat_name)
nifti_tool -copy_im -prefix $results_dir/$subject/anat/MPRAGE_t1.nii -infiles ${anat_arr[0]}
echo "anatomical image: ${anat_arr[0]}" >> $results_dir/$subject/check/images_used_pat2.txt


#copy the first in the list of EPI-images found
func_name=$(find $first_dir -name cmrrmbep2dresting*| sort) 
echo $func_name
func_arr=($func_name)
nifti_tool -copy_im -prefix $results_dir/$subject/func/EPI_t2.nii -infiles ${func_arr[0]}
echo "functional image: ${func_arr[0]}" >> $results_dir/$subject/check/images_used.txt

#copy the two topup images
se_name=$(find $first_dir -name cmrrmbep2dse.nii.gz | sort) 
echo $se_name
se_arr=($se_name)
nifti_tool -copy_im -prefix $results_dir/$subject/topup/se.nii -infiles ${se_arr[0]}
echo "se image: ${se_arr[0]}" >> $results_dir/$subject/check/images_used.txt


seinv_name=$(find $first_dir -name cmrrmbep2dseinvpol.nii.gz| sort) 
echo $seinv_name
seinv_arr=($seinv_name)
nifti_tool -copy_im -prefix $results_dir/$subject/topup/seinv_ph.nii -infiles ${seinv_arr[0]}
echo "inv se: ${seinv_arr[0]}" >> $results_dir/$subject/check/images_used.txt

done #< ${1}
}

read_files #${subj_file}
