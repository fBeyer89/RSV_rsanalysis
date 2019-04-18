
from utils import check_if_wf_is_ok
import os, glob





#wd_path = '/scr/kansas1/liem/sample_5/wd'
#wd_path = '/nobackup/clustercache/liem/LIFE/wd'
#wd_path = '/data/liem-2/LIFE/wd'
wd_path = '/scr/adenauer2/Franz/LIFE_WD/wd'
root_dir = '/data/liem-1/LIFE/'

wf = 'lemon_resting'
batch_path_template = os.path.join(wd_path, '{subject_id}', wf, 'batch')
crash_path_template = os.path.join(wd_path, '{subject_id}', 'crash_files')
check_file_list = [root_dir + '/preprocessed/{subject_id}/resting_state/ants/rest_mni_unsmoothed_fullspectrum.nii.gz']

os.chdir(wd_path)
subjects_list = glob.glob('LI*')


everything_ok, df_crashed = check_if_wf_is_ok(batch_path_template, crash_path_template, subjects_list)


print('\n\n CHECKING FOR MISSING FILES...')
missing_files = False
for subject_id in subjects_list:
    for file_template in check_file_list:
        subject_file = file_template.format(subject_id=subject_id)
        if not os.path.exists(subject_file):
            print('%s MISSING FILE'%subject_id)
            missing_files = True

if missing_files:
    print('\n SOME FILES MISSING')
else:
    print('\n ALL OK: files are there')
