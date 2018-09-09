#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/28 12:55
# @Author  : Hongjian Kang
# @File    : gen_2d_from_3d_pickle.py

#将pickle文件中存储的3d 64*64*64 suv、ct图像块分为64个64*64的slice存在文件中
import os
import pickle as pkl
from scipy.misc import imsave

def save_2d_from_3d(pickle_path, save_path):  # pickle_path为pickle文件绝对路径
    print('Processing  {}'.format(pickle_path))
    name = os.path.split(pickle_path)[-1].split('.')[0]
    with open(pickle_path, 'rb') as f:
        array = pkl.load(f)
    for i in range(array.shape[3]):
        imsave(os.path.join(save_path, name+'_{:>02}.png'.format(i+1)), array[0, :, :, i, 0])

def main():
    ct_space = r'E:\training data\3D volume new(64+64)\ct volume'
    pt_space = r'E:\training data\3D volume new(64+64)\pt volume'
    ct_paths = [os.path.join(ct_space, _) for _ in os.listdir(ct_space)]
    pt_paths = [os.path.join(pt_space, _) for _ in os.listdir(pt_space)]

    hu_save_path = r'E:\training data\Hengjian Yu\Hu'
    suv_save_path = r'E:\training data\Hengjian Yu\SUV'
    if not os.path.exists(hu_save_path):
        os.mkdir(hu_save_path)
    if not os.path.exists(suv_save_path):
        os.mkdir(suv_save_path)
    
    for ct_path in ct_paths:
        save_2d_from_3d(ct_path, hu_save_path)
    for pt_path in pt_paths:
        save_2d_from_3d(pt_path, suv_save_path)


if __name__ == '__main__':
    main()