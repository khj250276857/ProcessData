#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 14:30
# @Author  : Hongjian Kang
# @File    : gen_ct_image_with_slope.py

import pydicom as pdm
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from scipy.misc import imsave


def get_ct_array(file_path):
    # 获得一个文件目录下的所有ct图像序列的ndarray，
    # CT_value = pixel_value * slope + intercept
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        raise ValueError('Given file_path does not exist or is not a file: ' + file_path)
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    Pixel, slopes, intercepts, ct_array = [], [], [], []
    for file_name in file_names:
        ds = pdm.read_file(file_name)
        Pixel.append(ds.pixel_array)
        slopes.append(ds.get('RescaleSlope'))
        intercepts.append(ds.get('RescaleIntercept'))
    Pixel = np.array(Pixel)
    slopes = np.array(slopes)
    intercepts = np.array(intercepts)

    for i in range(Pixel.shape[0]):
        ct_array.append(Pixel[i, :, :] * slopes[i] + intercepts[i])
    return np.array(ct_array, dtype='float32')


def resize(input_array):
    output_array = []
    for i in range(input_array.shape[0]):
        output_array.append(cv2.resize(input_array[i], (128, 128), interpolation=cv2.INTER_CUBIC))
    output_array = np.array(output_array, dtype='float32')
    return output_array


def normolize(input_array):
    max_pixel = input_array.max()
    min_pixel = input_array.min()
    for i in range(input_array.shape[0]):
        input_array[i] = (input_array[i]-min_pixel)/(max_pixel-min_pixel)*255
    return input_array


def clip(input_array, low, high):
    output_array = input_array * (input_array <= high)
    output_array = np.clip(output_array, low, output_array.max())
    return output_array

def main():
    worksapce = r'E:\实验数据\2018_05_14_脱敏后PETCT 91例\PT00704-5\CT'
    save_path = r'E:\training data\新建文件夹'
    ct_array = get_ct_array(worksapce)
    ct_array = ct_array.transpose((1, 2, 0))
    # ct_array = clip(ct_array, -90, 95)
    ct_array = resize(ct_array)
    # ct_array = normolize(ct_array).reshape(ct_array.shape[0], ct_array.shape[1], ct_array.shape[2], 1)
    # ct_array_equal = cv2.equalizeHist(ct_array[50])
    # print(ct_array_equal.shape)

    # ct_array = np.clip(ct_array, -50, 110)
    # imsave(os.path.join(save_path, '-100-500.png'), ct_array[100])
    print(ct_array.shape)
    plt.figure()
    plt.imshow(ct_array[64, :, :], cmap='gray')
    plt.show()



if __name__ == '__main__':
    main()