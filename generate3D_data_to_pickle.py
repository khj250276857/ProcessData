#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/1 21:02
# @Author  : Hongjian Kang
# @File    : generate3D_test.py

import pickle as pkl
import pydicom as pdm
import numpy as np
import os
import cv2

# 遍历91个患者CT、PET所有图像，生成对应的3D图像块数据存在pickle文件中

def normalize(input_array):
    input_array = (input_array - np.mean(input_array)) / np.std(input_array)
    input_array = (input_array - np.min(input_array)) / (np.max(input_array) - np.min(input_array))
    return input_array


def resize(input_array):
    output_array = []
    for i in range(input_array.shape[0]):
        output_array.append(cv2.resize(input_array[i], (128, 128), interpolation=cv2.INTER_CUBIC))
    output_array = np.array(output_array, dtype='float32')
    return output_array

def gen_3d_volume(ct_array, pt_array, patch_size: int, pixel_spacing:int, ct_save_path, pt_save_path, start_num):
    '''
    同时对一个患者的3D pet和ct数据进行裁剪，并转置为[1,h,w,d,c],将图像块对存入对应文件夹的pickle文件中
    :param ct_array: 相同患者全部pet数据生成的ndarray, [1,d,h,w,c]
    :param pt_array: 相同患者全部pet数据生成的ndarray, [1,d,h,w,c]
    :param patch_size: 想要裁剪的图像块size大小
    :param pixel_spacing: h,w,d轴上裁剪间隔像素
    :param ct_save_path: ct volume保存文件夹，绝对路径
    :param pt_save_path: pt volume保存文件夹，绝对路径
    :param start_num: 图像保存路径起始编号
    :return: pickle文件
    '''
    height_iter = (ct_array.shape[1] - patch_size) // pixel_spacing + 1
    width_iter = (ct_array.shape[2] - patch_size) // pixel_spacing + 1
    depth_iter = (ct_array.shape[3] - patch_size) // pixel_spacing + 1

    temp = 0
    for i in range(height_iter):
        for j in range(width_iter):
            for k in range(depth_iter):
                temp_ct_array = ct_array[0:, pixel_spacing * i:pixel_spacing * i + patch_size,
                                pixel_spacing * j:pixel_spacing * j + patch_size, pixel_spacing * k:pixel_spacing * k + patch_size, 0:]
                temp_pt_array = pt_array[0:, pixel_spacing * i:pixel_spacing * i + patch_size,
                                pixel_spacing * j:pixel_spacing * j + patch_size, pixel_spacing * k:pixel_spacing * k + patch_size, 0:]
                ct_save_folder = os.path.join(ct_save_path, '{:>05}.pkl'.format(start_num + temp + 1))
                pt_save_folder = os.path.join(pt_save_path, '{:>05}.pkl'.format(start_num + temp + 1))
                with open(ct_save_folder, 'wb') as f:
                    pkl.dump(temp_ct_array, f)
                with open(pt_save_folder, 'wb') as f:
                    pkl.dump(temp_pt_array, f)
                temp += 1
    return temp

def getCTarrayFromFile(file_path):
    # 读取文件中的CT文件夹的全部CT图像，返回三维ndarray， 例如 file_path = r'E:\实验数据\2018_05_14_脱敏后PETCT 91例\PT00704-5'
    ct_file_path = os.path.join(file_path, 'CT')
    ct_file_names = [os.path.join(ct_file_path, _) for _ in os.listdir(ct_file_path)]
    ct_array = []
    for ct_file_name in ct_file_names:
        ct_array.append(pdm.read_file(ct_file_name).pixel_array)
    ct_array = np.array(ct_array, dtype='float32')
    ct_array = normalize(np.clip(resize(ct_array), 500, ct_array.max()))
    ct_array = ct_array.reshape(1, ct_array.shape[0], ct_array.shape[1], ct_array.shape[2], 1)
    ct_array = ct_array.transpose(0, 2, 3, 1, 4)

    return ct_array

def getPTarrayFromFile(file_path):
    pt_file_path = os.path.join(file_path, 'PT')
    pt_file_names = [os.path.join(pt_file_path, _) for _ in os.listdir(pt_file_path)]
    pt_array = []
    for pt_file_name in pt_file_names:
        pt_array.append(pdm.read_file(pt_file_name).pixel_array)
    pt_array = normalize(np.array(pt_array, dtype='float32'))
    pt_array = pt_array.reshape(1, pt_array.shape[0], pt_array.shape[1], pt_array.shape[2], 1)
    pt_array = pt_array.transpose(0, 2, 3, 1, 4)

    return pt_array

def main():
    workspace = r'E:\实验数据\2018_05_14_脱敏后PETCT 91例'
    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace)]

    ct_save_path = r'E:\training data\3D volume\ct volume'
    pt_save_path = r'E:\training data\3D volume\pt volume'
    if not os.path.exists(ct_save_path):
        os.mkdir(ct_save_path)
    if not os.path.exists(pt_save_path):
        os.mkdir(pt_save_path)

    start_num = 0
    pixel_spacing = 32
    file_num = len(file_paths)
    for i in range(file_num):
        print('processing {}/{}:   {}'.format(i, file_num, file_paths[i]))
        print('start_num:  {}'.format(start_num))
        ct_array = getCTarrayFromFile(file_paths[i])
        pt_array = getPTarrayFromFile(file_paths[i])
        start_num += gen_3d_volume(ct_array, pt_array, 64, pixel_spacing, ct_save_path, pt_save_path, start_num)


if __name__ == '__main__':
    main()

