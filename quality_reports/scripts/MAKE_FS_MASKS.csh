#!/bin/csh
# This script creates WM and V and WB and GRAY masks from Freesurfer segmentations.
# The first input is the VC#
# The second input is the voxel size, e.g., 222 or 333
# The third input is the directory where the /FREESURFER folders are found
# For example, 'MAKE_FS_MASKS.csh vc11111 222 /free/surfer/here/' runs the script creating 222 masks.
# For this, we only need the /mri folder from FREESURFER
# Output will be written to $basedir/$subject/nusmask/
#
# This makes a grey matter ribbin, a whole brain mask, and several erosions of CSF and WM masks, including no erosion.
# JDP 8/14/12, modified from TOL script.

setenv FSLOUTPUTTYPE NIFTI_GZ

set subject = $1
set voxdim = $2
set basedir = $3
set subjectdir = ${basedir}/${subject}/mri/
set outputdir = ${basedir}/${subject}/nusmask

echo $subjectdir
echo $outputdir

mkdir $outputdir
chmod g+w $outputdir
set file  = aparc+aseg

pushd ${subjectdir}

#Convert segmentation file to nifti and move to output directory
mri_convert -rl rawavg.mgz ${file}.mgz ${file}.nii
mv ${file}.nii ${outputdir}
cd ${outputdir}



## WHOLE BRAIN MASK ##

# binarize the freesurfer image to create a custom brain mask
fslmaths ${file} -bin ${file}_brainmask
gunzip -f ${file}_brainmask.nii.gz
nifti_4dfp -4 ${file}_brainmask ${file}_brainmask.4dfp.img
t4img_4dfp none ${file}_brainmask.4dfp.img ${file}_brainmask_${voxdim} -0${voxdim}
maskimg_4dfp -t0 -v1 ${file}_brainmask_${voxdim} ${file}_brainmask_${voxdim} ${file}_brainmask_mask_${voxdim}
rm ${file}_brainmask.nii ${file}_brainmask.4dfp* ${file}_brainmask_${voxdim}.4dfp*



## WHITE MATTER MASKS, ERODED ##

set cerebralwm = (2 41)
set eroiterwm = (6)

#Select each region from segmentation: cerebral white matter
foreach region (${cerebralwm})	
	fslmaths ${file}.nii -thr $region -uthr $region ${file}_reg${region}.nii
end

#Add regions together into one mask
fslmaths ${file}_reg${cerebralwm[1]}.nii.gz -add ${file}_reg$cerebralwm[2].nii.gz ${file}_cerebralwm
fslmaths ${file}_cerebralwm -bin ${file}_cerebralwm

#Erode cerebral white matter mask to avoid possible gray matter contamination
set iter = 0
gunzip -f ${file}_cerebralwm.nii.gz
nifti_4dfp -4 ${file}_cerebralwm ${file}_cerebralwm.4dfp.img
t4img_4dfp none ${file}_cerebralwm.4dfp.img ${file}_cerebralwm_${voxdim} -0${voxdim}
maskimg_4dfp -t0 -v1 ${file}_cerebralwm_${voxdim} ${file}_cerebralwm_${voxdim} ${file}_cerebralwm_ero${iter}_mask_${voxdim}

set iter = 1
while ( $iter <= ${eroiterwm} )
	fslmaths ${file}_cerebralwm -kernel 3D -ero ${file}_cerebralwm
	gunzip -f ${file}_cerebralwm.nii.gz
	nifti_4dfp -4 ${file}_cerebralwm ${file}_cerebralwm.4dfp.img
	t4img_4dfp none ${file}_cerebralwm.4dfp.img ${file}_cerebralwm_${voxdim} -0${voxdim}
	maskimg_4dfp -t0 -v1 ${file}_cerebralwm_${voxdim} ${file}_cerebralwm_${voxdim} ${file}_cerebralwm_ero${iter}_mask_${voxdim}
	@ iter++
end
rm ${file}_cerebralwm.* ${file}_cerebralwm_${voxdim}.*



## CSF MASKS, ERODED ##

set CSF = (4 5 14 15 24 43 44)
set eroiterCSF = (4)

#Select each region from segmentation: CSF
foreach region (${CSF})	
	fslmaths ${file}.nii -thr $region -uthr $region ${file}_reg${region}.nii
end

#Add regions together into one mask
cp ${file}_reg${CSF[1]}.nii.gz ${file}_CSF.nii.gz
set CSF_mask = ${file}_CSF.nii.gz
set r = 2
while ( $r <= 7 )
	fslmaths ${CSF_mask} -add ${file}_reg${CSF[$r]}.nii.gz ${CSF_mask}
	@ r++
end
fslmaths ${file}_CSF -bin ${file}_CSF
rm ${file}_reg*

#Erode CSF
set iter = 0
gunzip -f ${file}_CSF.nii.gz
nifti_4dfp -4 ${file}_CSF ${file}_CSF.4dfp.img
t4img_4dfp none ${file}_CSF.4dfp.img ${file}_CSF_${voxdim} -0${voxdim}
maskimg_4dfp -t0 -v1 ${file}_CSF_${voxdim} ${file}_CSF_${voxdim} ${file}_CSF_ero${iter}_mask_${voxdim}

set iter = 1
while ( $iter <= ${eroiterCSF} )
	fslmaths ${file}_CSF -kernel 3D -ero ${file}_CSF
	gunzip -f ${file}_CSF.nii.gz
	nifti_4dfp -4 ${file}_CSF ${file}_CSF.4dfp.img
	t4img_4dfp none ${file}_CSF.4dfp.img ${file}_CSF_${voxdim} -0${voxdim}
	maskimg_4dfp -t0 -v1 ${file}_CSF_${voxdim} ${file}_CSF_${voxdim} ${file}_CSF_ero${iter}_mask_${voxdim}
	@ iter++
end

rm ${file}_CSF.* ${file}_CSF_${voxdim}.*

rm ${file}.nii

popd



## GREY RIBBON ##

set GM = (3 42)
set file = aseg

pushd ${subjectdir}

#Convert file to nifti and move to output directory
mri_convert -rl rawavg.mgz ${file}.mgz ${file}.nii
mv ${file}.nii ${outputdir}
cd ${outputdir}

#Select each region from segmentation: cerebral white matter
foreach region (${GM})	
	fslmaths ${file}.nii -thr $region -uthr $region ${file}_reg${region}.nii
end

#Add regions together into one mask
fslmaths ${file}_reg${GM[1]}.nii.gz -add ${file}_reg$GM[2].nii.gz ${file}_GM
fslmaths ${file}_GM -bin ${file}_GM

gunzip -f ${file}_GM.nii.gz
nifti_4dfp -4 ${file}_GM ${file}_GM.4dfp.img
t4img_4dfp none ${file}_GM.4dfp.img ${file}_GM_${voxdim} -0${voxdim}
maskimg_4dfp -t0 -v1 ${file}_GM_${voxdim} ${file}_GM_${voxdim} ${file}_GM_mask_${voxdim}

rm ${file}_GM.nii ${file}_GM.4dfp* ${file}_GM_${voxdim}.4dfp* ${file}_reg${GM[1]}.nii.gz ${file}_reg${GM[2]}.nii.gz 
rm ${file}.nii

popd



