# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 11:21:34 2017

@author: fbeyer
"""

import numpy as N
import os,sys
import matplotlib.pyplot as plt


realignpar='/nobackup/aventurin3/data_fbeyer/RSV/3T/preprocessing/preprocessed/RSV003/resting_state/realign/rest_realigned.par'

def calc_frame_dispalcement(realignment_parameters_file, parameter_source):
    lines = open(realignment_parameters_file, 'r').readlines()
    rows = [[float(x) for x in line.split()] for line in lines]
    cols = np.array([list(col) for col in zip(*rows)])

    print(N.shape(cols))
    if parameter_source == 'AFNI':
        translations = N.transpose(N.abs(N.diff(cols[0:3, :])))
        rotations = N.transpose(N.abs(N.diff(cols[3:6, :])))
    
    elif parameter_source == 'FSL':
        translations = N.transpose(N.abs(N.diff(cols[3:6, :])))
        rotations = N.transpose(N.abs(N.diff(cols[0:3, :])))
        rotations_raw=rotations

    rot_transformed=(2*50*N.pi/360)*rotations;
    
    FD_power = N.sum(translations, axis = 1) + (2*50*N.pi/360)*N.sum(rotations, axis =1)
    FD_sum_transl=N.sum(translations, axis = 1)
    FD_sum_rots=N.sum(rotations, axis =1)
    #FD is zero for the first time point
    FD_power = N.insert(FD_power, 0, 0)
    FD_sum_transl=N.insert(FD_sum_transl,0,0)
    translations=N.insert(translations,0, 0, axis=0)
    rotations=N.insert(rotations,0, 0, axis=0)
    rot_transformed=N.insert(rot_transformed,0, 0, axis=0)
    print(N.shape(rot_transformed))
    #print(N.shape(FD_power))
    #print(N.shape(FD_sum_transl))
    return FD_power,FD_sum_transl,FD_sum_rots,translations,rotations_raw,rot_transformed
    
    
def compute_fd(realignment_parameters_file):

    motpars = N.loadtxt(realignment_parameters_file)
    print(N.shape(motpars))
    # compute absolute displacement
    dmotpars=N.zeros(motpars.shape)
    
    dmotpars[1:,:]=N.abs(motpars[1:,:] - motpars[:-1,:])#from first on.
    print N.shape(dmotpars)
    # convert rotation to displacement on a 50 mm sphere
    # mcflirt returns rotation in radians
    # from Jonathan Power:
    #The conversion is simple - you just want the length of an arc that a rotational
    # displacement causes at some radius. Circumference is pi*diameter, and we used a 5
    # 0 mm radius. Multiply that circumference by (degrees/360) or (radians/2*pi) to get the 
    # length of the arc produced by a rotation.
    
    #for test purposes convert rotational "radians" to degree
    
    
    headradius=50
    disp=dmotpars.copy()
    disp[:,0:3]=N.pi*headradius*2*(disp[:,0:3]/(2*N.pi)) #correct for FSL as rotational values are the first 3
    
    FD=N.sum(disp,1)
    
    trans=disp[:,3:6]
    rots=dmotpars.copy()
    rots=rots[:,0:3]
    FD_trans=N.sum(trans,1)
    FD_rots=N.sum(rots,1)
    
    
    return FD,FD_trans,FD_rots,disp,rots
    
FD_julia,FD_j_t,FD_rots_j,translations,rotations_raw,rot_transformed=calc_frame_dispalcement(realignpar,'FSL')
FD_poldrack,FD_po_t,FD_rots_po,disp,rots=compute_fd(realignpar)

#translational values are the same:
print(sum(FD_j_t-FD_po_t))

#raw rotational values are the same:
#print(sum(FD_rots_j-FD_rots_po))

#rotational raw values are the same:
print(sum(FD_julia-FD_poldrack))

plt.figure
plt.plot(disp[:,0],'bx')
plt.plot(rot_transformed[:,0]*57.2957,'ro')
plt.show()

plt.figure
plt.plot(disp[:,1],'bx')
plt.plot(rot_transformed[:,1]*57.2957,'ro')
plt.show()

plt.figure
plt.plot(disp[:,2],'bx')
plt.plot(rot_transformed[:,2]*57.2957,'ro')
plt.show()

#plt.figure
#plt.plot(disp[:,2]-rotations[:,2],'bx')
#plt.plot(disp[:,1]-rot_transformed[:,1],'gx')
#plt.plot(disp[:,0]-rotations[:,0],'yx')
#plt.figure
#plt.plot(FD_julia, 'rx',label='FD Julia')
#plt.plot(FD_poldrack, 'b', label='FD Poldrack')
#plt.legend(loc=2)
#plt.show()
#
#print(N.mean(FD_julia))
#print(N.mean(FD_poldrack))
#
#print(N.mean(FD_julia)/N.mean(FD_poldrack))