
import os, glob
import nibabel as nb


root_path = '/scr/kennedy2/liem/sample_5/subjects'

check_file_list = [os.path.join(root_path, '{subject_id}/unwarp/B0_mag.nii'),
                   os.path.join(root_path, '{subject_id}/unwarp/B0_ph.nii')]

os.chdir(root_path)
subjects_list = glob.glob('LI*')
bad_subj = []

for subject_id in subjects_list:
    print(subject_id)
    for file_template in check_file_list:
        subject_file = file_template.format(subject_id=subject_id)

        im_shape = nb.load(subject_file).get_shape()
        if im_shape[2] != 30:
            bad_subj.append('%s: %s'%(subject_id, subject_file))

print('\n\n\n')
print(bad_subj)
