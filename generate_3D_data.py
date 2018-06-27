#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/24 18:09
# @Author  : Hongjian Kang
# @File    : generate_3D_data.py

'''
生成三维数据，用于训练网络
'''

import pydicom as pdm
import numpy as np
import os

def crop(input_array, n, d, w, h):
    '''
    将输入的3D图像块随机裁剪成多个小块
    :param input_array: 一个患者的全部图像序列生成的ndarray，reshape为1,d,w,h,c, typically c = 1
    :param n: number of patches，图像块的个数
    :param d: depth，图像块的深度，对应切片数
    :param w: width，图像块的宽度
    :param h: height，图像块的高度
    :return: 该患者数据生成的n个图像块的ndarray，shape:n,d,w,h,c, typically c = 1
    '''
    if input_array.shape[1] < d or input_array.shape[2] < w or input_array.shape[3] < h:
        raise('Expected image size larger than original image size')
    output_array = np.zeros([1, d, w, h, 1])
    # if output_array.shape == input_array.shape:
    #     print('peipeipei')
    for i in range(n):
        depth_temp = np.random.randint(d // 2, input_array.shape[1] - d // 2)
        width_temp = np.random.randint(w // 2, input_array.shape[2] - w // 2)
        height_temp = np.random.randint(h // 2, input_array.shape[3] - h // 2)
        new_array = input_array[0:, depth_temp-d//2:depth_temp+d//2, width_temp-w//2:width_temp+w//2, height_temp-h//2:height_temp+h//2, 0:]
        output_array = np.append(output_array, new_array, axis=0)
    return output_array[1:]

def crop_by_pixel(input_array, pixel, d, w, h):
    '''
    将输入的3D图像块每隔pixel个像素裁剪小块
    :param input_array: 一个患者的全部图像序列生成的ndarray，reshape为1,d,w,h,c, typically c = 1
    :param pixel: 每次裁剪间隔的像素个数
    :param d: depth，图像块的深度，对应切片数
    :param w: width，图像块的宽度
    :param h: height，图像块的高度
    :return: 该患者数据生成的n个图像块的ndarray，shape:n,d,w,h,c, typically c = 1
    '''

    if input_array.shape[1] < d or input_array.shape[2] < w or input_array.shape[3] < h:
        raise('Expected image size larger than original image size')
    output_array = np.zeros([1, d, w, h, 1])
    depth_iter = (input_array.shape[1] - d) // pixel
    width_iter = (input_array.shape[2] - w) // pixel
    height_iter = (input_array.shape[3] - h) // pixel
    for i in range(depth_iter):
        for j in range(width_iter):
            for k in range(height_iter):
                new_array = input_array[0:, pixel*i:pixel*i+d, pixel*j:pixel*j+w, pixel*k:pixel*k+h, 0:]
                output_array = np.append(output_array, new_array, axis=0)
    return output_array[1:]


def main():
    workspace = r'E:\实验数据\2018_05_14_脱敏后PETCT 91例\PT00704-5\PT'
    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace)]
    L = []
    for file_path in file_paths:
        img_array = pdm.read_file(file_path).pixel_array
        L.append(img_array)
    img = np.array(L)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2], 1))
    # new_img = crop(img, 10, 32, 32, 32)
    new_img = crop_by_pixel(img, 20, 32, 32, 32)


if __name__ == '__main__':
    main()