#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/2 15:15
# @Author  : Hongjian Kang
# @File    : load3D_test.py

import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt

def main():
    ct_pkl_dir = r'E:\training data\3D volume\ct volume\00005.pkl'
    pt_pkl_dir = r'E:\training data\3D volume\pt volume\00005.pkl'
    with open(ct_pkl_dir, 'rb') as f:
        ct_array = pkl.load(f)
    with open(pt_pkl_dir, 'rb') as f:
        pt_array = pkl.load(f)

    ct_array = ct_array.reshape(ct_array.shape[1], ct_array.shape[2], ct_array.shape[3])
    pt_array = pt_array.reshape(pt_array.shape[1], pt_array.shape[2], pt_array.shape[3])
    ct_slice = ct_array[:, :, 32]
    pt_slice = pt_array[:, :, 32]
    plt.figure('ct_slice')
    plt.imshow(ct_slice, cmap='gray')
    plt.figure('pt_slice')
    plt.imshow(pt_slice, cmap='gray')
    plt.show()

if __name__ == '__main__':
    main()

