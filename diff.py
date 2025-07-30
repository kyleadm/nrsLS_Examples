#! /usr/bin/env python
#
# A script that compares two NekRS output (.f00000) files --> note that
# it only operates on the .f00000 files because we need the mesh data
# which is only written in the very first NekRS output file.
#
# More details using Pymech can be found at the following link:
# https://github.com/eX-Mech/pymech?tab=readme-ov-file
#
# author: Kyle A. Damm
# date:   29-07-2025
#

import pymech as pm
import numpy as np
import matplotlib.pyplot as plt

def get_data(filename):
    # read in the Nekrs .f file
    data = pm.open_dataset(filename)
    print(data)

    # pull out the x coordinate of the nodes along with the values for S02 at the last step
    X = np.array(data.xmesh.stack(k=("x", "y", "z")), dtype=np.float64)
    S01 = np.array(data.s01.stack(k=("x", "y", "z")), dtype=np.float64)
    data = np.array([X[:], S01[:]]).T
    data = sorted(data, key=lambda x: x[0]) # sort data by X
    x = [x[0] for x in data]
    s01 = [x[1] for x in data]
    return np.array([x, s01])

def plot(x, y):
    plt.plot(x, y, linewidth=3.0, color='black')
    plt.xlabel("x", fontsize=12)
    plt.ylabel("y", fontsize=12)
    plt.show()

if __name__=='__main__':

    # read in the Nekrs .f file
    data1 = get_data('ref.f00000')
    data2 = get_data('sine0.f00000')

    # evaluate the L2 error norm
    abs_diff_f = np.abs(data1[1]-data2[1])
    L2_error_f = np.sqrt(np.dot(abs_diff_f,abs_diff_f))
    print("L2 error norm: ", L2_error_f)

    # plot error
    plot(data1[0], abs_diff_f)




