import os

if __name__ == '__main__':

    data_path = "/data/pt_nro132/nil2/reinelt/NECOS/MRI/"
    nil2_dir='/scr/nil2/reinelt/NECOS'
    #test_dir = "/scr/nil2/reinelt/NECOS/MRI/test"

    with open('/scr/nil2/reinelt/NECOS/subject_list.txt', 'r') as f:
        subjects = [line.strip() for line in f]
    subjects.sort()

    scan_id_list = [ 'rest2', 'rest3'] #'rest1', 'rest2', 'rest3', 'rest4', 'rest5', 'rest6',

    for subject in subjects:
        #print(subject)

        for scan in scan_id_list:
            #scrub_file = data_dir + '/' + subject + '/preprocessed/functional/' + scan + '_QA/report_Power/scrubvols.txt'
            #print(scrub_file)
            
            trimmed_file = nil2_dir + '/scrubbed_scans/' + subject + '/' + scan + '/trimmed_filtered_func_data.nii.gz'
            print(trimmed_file)
            
            #import os
            if os.path.isfile(trimmed_file):
                print('lala')
                mri_dir =  nil2_dir + '/MRI/' + subject + '/' + scan
                os.makedirs(mri_dir)
            else:
                print('nono')
