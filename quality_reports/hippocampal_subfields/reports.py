def create_report(subject_id, anat_brain,subfield, output_file):
    import gc
    import pylab as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from plot_subfields import plot_hipp_subfields

    
    
    report = PdfPages(output_file)    

    
    fig = plot_hipp_subfields(anat_brain, subfield, figsize=(8.3, 8.3))
    report.savefig(fig, dpi=300)
    fig.clf()
    plt.close()
    
    report.close()
    gc.collect()
    plt.close()
    
    return output_file, subject_id



def read_dists(csv_file):
    
    import pandas as pd
    import numpy as np
    df = pd.read_csv(csv_file, dtype=object)
    sim = dict(zip(df['subject_id'], list(np.asarray(df['coregistration quality'], dtype='float64'))))
    mfd = list(np.asarray(df['Mean FD'], dtype='float64'))
    tsnr = list(np.asarray(df['Median tSNR'], dtype='float64'))
    
    return sim, mfd, tsnr


def check(subject_id,checklist):
    
    with open(checklist, 'a') as f:
        f.write(subject_id+'\n')
    return checklist
