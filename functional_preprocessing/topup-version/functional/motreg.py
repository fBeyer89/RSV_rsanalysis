# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:38:21 2015

@author: fbeyer
"""


def motion_regressors(motion_params, order=0, derivatives=1):
    """From https://github.com/nipy/nipype/blob/master/examples/
    rsfmri_vol_surface_preprocessing_nipy.py#L261
    Compute motion regressors upto given order and derivative
    motion + d(motion)/dt + d2(motion)/dt2 (linear + quadratic)
    """
    from nipype.utils.filemanip import filename_to_list
    import numpy as np
    import os
    out_files = []
    for idx, filename in enumerate(filename_to_list(motion_params)):
        params = np.genfromtxt(filename)
        out_params = params
        for d in range(1, derivatives + 1):
            cparams = np.vstack((np.repeat(params[0, :][None, :], d, axis=0),
                                 params))
            out_params = np.hstack((out_params, np.diff(cparams, d, axis=0)))
        out_params2 = out_params
        for i in range(2, order + 1):
            out_params2 = np.hstack((out_params2, np.power(out_params, i)))
        filename = os.path.join(os.getcwd(), "motion_regressor%02d.txt" % idx)
        np.savetxt(filename, out_params2, fmt="%.10f")
        out_files.append(filename)
    return out_files




def calc_friston_twenty_four(in_file):
    """
    from https://github.com/FCP-INDI/C-PAC/blob/master/CPAC/generate_motion_statistics/generate_motion_statistics.py
    Method to calculate friston twenty four parameters

    Parameters
    ----------
    in_file: string
        input movement parameters file from motion correction

    Returns
    -------
    new_file: string
        output 1D file containing 24 parameter values

    """

    import numpy as np
    import os

    new_data = None

    data = np.genfromtxt(in_file)

    data_squared = data ** 2

    new_data = np.concatenate((data, data_squared), axis=1)

    data_roll = np.roll(data, 1, axis=0)

    data_roll[0] = 0

    new_data = np.concatenate((new_data, data_roll), axis=1)

    data_roll_squared = data_roll ** 2

    new_data = np.concatenate((new_data, data_roll_squared), axis=1)

    new_file = os.path.join(os.getcwd(), 'fristons_twenty_four.1D')
    np.savetxt(new_file, new_data, fmt='%0.8f', delimiter=' ')

    return new_file

