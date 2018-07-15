#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/2 15:15
# @Author  : Hongjian Kang
# @File    : load3D_test.py

import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imsave
import os

def main():
    x_dir = r'E:\training data\running data\validate\2_x.pkl'
    y_dir = r'E:\training data\running data\validate\2_y.pkl'
    z_dir = r'E:\training data\running data\validate\2_z1.pkl'
    save_path = r'E:\training data\新建文件夹'

    with open(x_dir, 'rb') as f:
        batch_x = pkl.load(f)
    with open(y_dir, 'rb') as f:
        batch_y = pkl.load(f)
    with open(z_dir, 'rb') as f:
        batch_z = pkl.load(f)

    # ct_array = ct_array.reshape(ct_array.shape[1], ct_array.shape[2], ct_array.shape[3])
    # pt_array = pt_array.reshape(pt_array.shape[1], pt_array.shape[2], pt_array.shape[3])
    img_x = batch_x[:, :, 32]
    img_y = batch_y[:, :, 32]
    img_z = batch_z[:, :, 32]
    imsave(os.path.join(save_path, '2_x.png'), img_x)
    imsave(os.path.join(save_path, '2_y.png'), img_y)
    imsave(os.path.join(save_path, '2_z.png'), img_z)

    # plt.figure('img_x')
    # plt.imshow(img_x, cmap='gray')
    # plt.figure('img_y')
    # plt.imshow(img_y, cmap='gray')
    # plt.figure('img_z')
    # plt.imshow(img_z, cmap='gray')
    # plt.show()

if __name__ == '__main__':
    main()

