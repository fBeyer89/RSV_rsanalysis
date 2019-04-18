from utils import check_if_wf_is_ok, load_subjects_list
import os, glob

root_dir = '/data/liem-1/LIFE/'

check_file_list = ['preprocessed/{subject_id}/resting_state/ants/rest_mni_unsmoothed_fullspectrum.nii.gz',
                   'preprocessed/{subject_id}/resting_state/ants/rest_mni_unsmoothed.nii.gz',
                   'preprocessed/{subject_id}/resting_state/denoise/rest_preprocessed_nativespace_fullspectrum.nii.gz',
                   'preprocessed/{subject_id}/resting_state/denoise/rest_preprocessed_nativespace.nii.gz',
                   'preprocessed/{subject_id}/resting_state/FWHM6/rest_mni_smoothed.nii.gz',
                   'preprocessed/{subject_id}/resting_state/realign/rest_realigned.par',
                   'preprocessed/{subject_id}/structural/transforms2mni/transform0GenericAffine.mat',
                   'preprocessed/{subject_id}/structural/transforms2mni/transform1InverseWarp.nii.gz',
                   'preprocessed/{subject_id}/structural/transforms2mni/transform1Warp.nii.gz',
                   ]

subjects_list = load_subjects_list('/scr/adenauer2/Franz/LIFE16/LIFE16_preprocessed_subjects_list_n2557.txt')
print subjects_list

print('\n\n CHECKING FOR MISSING FILES...')
missing_files = False
for subject_id in subjects_list:
    for file_template in check_file_list:
        subject_file = os.path.join(root_dir, file_template.format(subject_id=subject_id))
        # print subject_file
        if not os.path.exists(subject_file):
            print('MISSING FILE %s: %s' % (subject_id, subject_file))
            missing_files = True

if missing_files:
    print('\n SOME FILES MISSING')
else:
    print('\n ALL OK: files are there (%s subjects)' % len(subjects_list))
