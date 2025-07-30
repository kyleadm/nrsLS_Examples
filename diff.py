#! /usr/bin/env python
#
# A script that compares two NekRS output files.

# More details using Pymech can be found at the following link:
# https://github.com/eX-Mech/pymech?tab=readme-ov-file
#
# author: Kyle A. Damm
# date:   29-07-2025
#

import pymech as pm
import numpy as np
import matplotlib.pyplot as plt

def get_xcoord_data(filename):
    data = pm.readnek(filename)
    Nelem = len(data.elem)
    xlist = []
    for elem in data.elem:
       xlist.extend(elem.pos[0].ravel())
    return np.array(xlist)

def get_scalar_data(filename):
    data = pm.readnek(filename)
    Nelem = len(data.elem)
    slist = []
    for elem in data.elem:
        slist.extend(elem.scal[1].ravel())
    return np.array(slist)

def reorder_data(X, S):
    # pull out the x coordinate of the nodes along with the values for S02 at the last step
    data = np.array([X[:], S[:]]).T
    data = sorted(data, key=lambda x: x[0]) # sort data by X
    x = [x[0] for x in data]
    s = [x[1] for x in data]
    return np.array([x, s])

def plot(x, y):
    plt.plot(x, y, linewidth=3.0, color='black')
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.show()

if __name__=='__main__':

    # path to NekRS simulation directories to compare
    path1 = 'linear1D-serial'
    path2 = 'linear1D'

    # read in the x-coordinate data
    xdata1 = get_xcoord_data(path1+'/linear0.f00000')
    xdata2 = get_xcoord_data(path2+'/linear0.f00000')
    np.testing.assert_array_equal(xdata1, xdata2)

    # read in the scalar data
    sdata1 = get_scalar_data(path1+'/linear0.f00010')
    sdata2 = get_scalar_data(path2+'/linear0.f00010')

    # reorder data based on x-coordinate --> for nice plot
    data1 = reorder_data(xdata1, sdata1)
    data2 = reorder_data(xdata2, sdata2)

    # evaluate the L2 error norm
    abs_diff_f = np.abs(data1[1]-data2[1])
    L2_error_f = np.sqrt(np.dot(abs_diff_f,abs_diff_f))
    print("L2 error norm: ", L2_error_f)

    # plot error
    plot(data1[0], data1[1])
    plot(data2[0], data2[1])
    plot(data1[0], abs_diff_f)

