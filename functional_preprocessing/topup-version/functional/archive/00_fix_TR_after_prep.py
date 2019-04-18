import os, subprocess, glob, nibabel as nib, shutil
from datetime import datetime
from joblib import Parallel, delayed

n_cores = 20

root_path = '/data/liem-1/LIFE/preprocessed'
log_file_root = '/data/liem-1/LIFE/fix_tr_logs'
if not os.path.exists(log_file_root):
    os.makedirs(log_file_root)

TR = 2000  # TR in msec
TR_sec = TR / 1000.

file_list = ['ants/rest_mni_unsmoothed_fullspectrum.nii.gz',
             'ants/rest_mni_unsmoothed.nii.gz',
             'denoise/rest_preprocessed_nativespace_fullspectrum.nii.gz',
             'denoise/rest_preprocessed_nativespace.nii.gz',
             # 'FWHM6/rest_mni_smoothed.nii.gz',
             ]


def fix_TR_fs(s):
    print s

    for f_path in file_list:
        nii = os.path.join(root_path, s, 'resting_state', f_path)

        log_file_path_std = os.path.join(log_file_root, '%s_log_std.txt' % s)
        log_file_path_err = os.path.join(log_file_root, '%s_log_err.txt' % s)
        cmd = 'mri_convert -tr {TR} {nii} {nii} >> {log_file_std} 2>> {log_file_err}'.format(TR=TR, nii=nii,
                                                                                             log_file_std=log_file_path_std,
                                                                                             log_file_err=log_file_path_err)
        os.system(cmd)


os.chdir(root_path)
subjects_list = glob.glob('LI*')

t1 = datetime.now()

Parallel(n_jobs=n_cores)(delayed(fix_TR_fs)(s) for s in subjects_list)

t2 = datetime.now()
delta2 = (t2 - t1).seconds

print delta2
