#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 20:06
# @Author  : Hongjian Kang
# @Site    : 
# @File    : cal_SUV_for_GE.py
# @Software: PyCharm

'''
The formula we use for SUV factors are:(for GE)
SUVbw = pixel * bw/actual_activity ;
SUVbsa = pixel * bsa./actual_activity;
SUVlbm = píxel * lbm /actual_activity;  # 本实现中pixel = PET_Value * slope + intercept
bw = weight;
bsa = weight^0.425 * height^0.725 * 0.007184;
lbm = 1.10 * weight – 120 * (weight/height)^2 for male;
       = 1.07 * weight – 148 * (weight/height)^2 for female;
actual activity = [tracer_activity * 2^( -(scan_time – measured_time) / half_life) ]

'''

import pydicom as pdm
import numpy as np
import os
import time
import datetime
import matplotlib.pyplot as plt
from scipy.misc import imsave


def calSUV(pt_array, slopes, intercepts, baseInfo):
    '''
    给定一个患者所有PET图像计算SUV值
    :param pt_array: 某一患者全部PET图像像素值的三维ndarray
    :param slopes: 某一患者全部PET图像的斜率slopes组成的ndarray
    :param intercepts: 某一患者全部PET图像的截距intercepts组成的ndarray
    :param baseInfo: 某一患者的基本信息对象字典，dictionary{}
    :return: ndarray三维数组，表示SUV值，第一维为图像索引维，后两维为图像长宽
    '''

    lbmKg = baseInfo['lbm']     # 瘦体重
    actualActivity = baseInfo['actualDose']
    SUV = []
    for i in range(pt_array.shape[0]):
        SUV.append((pt_array[i, :, :] * slopes[i] + intercepts[i]) * lbmKg * 1000 / actualActivity)
    return np.array(SUV)


def gen_baseInfo(file_path):
    # 根据路径中的第一张PET图像生成基本信息对象，存在baseInfo中
    baseInfo = {}   # 计算SUV值所必须的基本属性
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    file_name = file_names[0]
    meta = pdm.read_file(file_name)     # 读取第一张PET图像头文件meta

    baseInfo['weight'] = meta.get('PatientWeight')   # PatientsWeight
    baseInfo['height'] = meta.get('PatientSize') * 100    # PatientSize(in cm)
    baseInfo['sex'] = meta.get('PatientSex')
    if baseInfo['sex'] == 'M':
        lbmKg = 1.10 * baseInfo['weight'] - 120 * (baseInfo['weight'] / baseInfo['height']) ** 2
    else:
        lbmKg = 1.07 * baseInfo['weight'] - 148 * (baseInfo['weight'] / baseInfo['height']) ** 2
    baseInfo['lbm'] = lbmKg

    if None != meta.get('RadiopharmaceuticalInformationSequence'):
        tracerActivity = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadionuclideTotalDose')
        theDate = meta.get('SeriesDate')
        measureTime = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadiopharmaceuticalStartTime')
        measureTime = time.strptime(theDate + measureTime[0:6], '%Y%m%d%H%M%S')
        measureTime = datetime.datetime(*measureTime[:6])   # RadiopharmaceuticalStartTime
        scanTime = meta.get('AcquisitionTime')
        scanTime = time.strptime(theDate + scanTime, '%Y%m%d%H%M%S')
        scanTime = datetime.datetime(*scanTime[:6])     # AcquisitionTime
        halfLife = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadionuclideHalfLife')    # RadionuclideHalfLife
        if (scanTime <= measureTime):
            raise ('time wrong:scanTime should be later than measure')
        else:
            actualActivity = tracerActivity * 2 ** (-((scanTime - measureTime).seconds) / halfLife)

        baseInfo['dose'] = tracerActivity
        baseInfo['actualDose'] = actualActivity
    return baseInfo


def get_pt_array(file_path):
    # 将一个患者路径下的所有PET图像的像素值读取出来，返回存在一个ndarray中
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        raise ValueError('Given file_path does not exist or is not a file: ' + file_path)
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    L = []
    for file_name in file_names:
        L.append(pdm.read_file(file_name).pixel_array)
    pt_array = np.array(L)
    return pt_array


def read_slopes(file_path):
    # 将一个患者路径下的所有pet图像的slope读取出来，返回存在一个ndarray中
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        raise ValueError('Given file_path does not exist or is not a file: ' + file_path)
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    slopes = []
    for file_name in file_names:
        ds = pdm.read_file(file_name)
        slopes.append(ds.get('RescaleSlope'))
    slopes = np.array(slopes)
    return slopes


def read_intercepts(file_path):
    # 将一个患者路径下的所有pt图像的intercepts读取出来，返回存在一个ndarray中
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        raise ValueError('Given file_path does not exist or is not a file: ' + file_path)
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    intercepts = []
    for file_name in file_names:
        ds = pdm.read_file(file_name)
        intercepts.append(ds.get('RescaleIntercept'))
    intercepts = np.array(intercepts)
    return intercepts

def save_image_from_array(save_path, input_array, start_num):
    for i in range(input_array.shape[0]):
        imsave(save_path+'/{:>05}.jpg'.format(start_num+i+1), input_array[i])


def main():
    workspace = r'E:\实验数据\2018_05_14_脱敏后PETCT 91例'
    #save_path = r''    todo: add it
    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace)]
    # file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace) if _.startswith('PT')]
    for i in range(len(file_paths)):
        file_paths[i] = [os.path.join(file_paths[i], _) for _ in os.listdir(file_paths[i]) if _.startswith('PT')][0]

    image_num = 0
    for file_path in file_paths:
        print('processing    '+file_path)
        baseInfo = gen_baseInfo(file_path)
        slopes = read_slopes(file_path)
        intercepts = read_intercepts(file_path)
        pt_array = get_pt_array(file_path)
        suv_array = calSUV(pt_array, slopes, intercepts, baseInfo)



    # image = suv_array[117, :, :]
    # plt.figure('PT_000')
    # plt.imshow(image, cmap='gray')
    # plt.show()




if __name__ == '__main__':
    main()


