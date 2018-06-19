import os
import pydicom as pdm
import numpy as np
import time
import datetime
import math
import matplotlib.pyplot as plt

'''
在西门子机器上计算SUV的方法是，都是标准的DICOM Tag
(0008,0032) [100209.015000]            # AcquisitionTime
(0010,1030) [75]            # PatientsWeight (kg)
(0018,1072) [090000.000000]          #  RadiopharmaceuticalStartTime
(0018,1074) [360100006.10352]              #  RadionuclideTotalDose (Bq)
(0018,1075) [6586.2]                    #  RadionuclideHalfLife (seconds)
(0028,1052) [0]                         #   RescaleIntercept
(0028,1053) [2.3295469284058]           #   RescaleSlope

Given X for a pixel value, Y= (RescaleIntercept + RescaleSlope X) exp(ln2*(AcqusitionTime- RadiopharmaceuticalStartTime)/ RadionuclideHalfLife)

SUV = Y/( RadionuclideTotalDose/ PatientsWeight)
需要注意的是，那个时间的格式是 小时分秒 hhmmss (0008,0032)
'''

# baseInfo = {}  # 计算SUV值所必须的基本属性

def calSUV(pt_array, slopes, intercepts, baseInfo):
    '''
    给定一个患者所有PET图像的array和slopes，计算SUV值
    :param pt_array: 某一患者全部PET图像像素值的三维ndarray
    :param slopes: 某一患者全部PET图像的斜率slopes组成的ndarray
    :param intercepts: 某一患者全部PET图像的截距intercepts组成的ndarray
    :return: ndarray三维数组，表示SUV值，第一维为图像索引维，后两维为图像长宽
    '''

    weight = baseInfo['weight']
    timeDiff = baseInfo['timeDiff']
    totalDose = baseInfo['totalDose']
    halfLife = baseInfo['halfLife']

    SUV = []
    for i in range(pt_array.shape[0]):
        Y = (pt_array[i, :, :] * slopes[i] + intercepts[i]) * math.exp(math.log(2) * timeDiff / halfLife)
        suv = Y / (totalDose / (weight * 1000))
        SUV.append(suv)
    return np.array(SUV)


def gen_baseInfo(file_path):
    # 根据路径中的第一张PET图像生成基本信息对象，存在baseInfo中
    baseInfo = {}   # 计算SUV值所必须的基本属性
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    file_name = file_names[0]
    meta = pdm.read_file(file_name)     # 读取第一张PET图像头文件meta

    baseInfo['weight'] = meta.get('PatientWeight')   # PatientsWeight
    baseInfo['height'] = meta.get('PatientSize') * 100    # PatientSize

    if None != meta.get('RadiopharmaceuticalInformationSequence'):
        totalDose = meta.get('RadiopharmaceuticalInformationSequence')[0].get('RadionuclideTotalDose')
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
        baseInfo['timeDiff'] = (scanTime - measureTime).seconds
        baseInfo['totalDose'] = totalDose
        baseInfo['halfLife'] = halfLife
    return baseInfo


def get_pt_array(file_path):
    # 将一个患者路径下的所有pt图像的像素值读取出来，返回存在一个ndarray中
    if not os.path.exists(file_path) or not os.path.isdir(file_path):
        raise ValueError('Given file_path does not exist or is not a file: ' + file_path)
    file_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
    L = []
    for file_name in file_names:
        L.append(pdm.read_file(file_name).pixel_array)
    pt_array = np.array(L)
    return pt_array


def read_slopes(file_path):
    # 将一个患者路径下的所有pt图像的slope读取出来，返回存在一个ndarray中
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


def main():
    workspace = r'E:\实验数据\2018_05_14_脱敏后PETCT 91例\PT00704-5'
    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace) if _.startswith('PT')]
    file_path = file_paths[0]
    baseInfo = gen_baseInfo(file_path)
    slopes = read_slopes(file_path)
    intercepts = read_intercepts(file_path)
    pt_array = get_pt_array(file_path)
    suv_array = calSUV(pt_array, slopes, intercepts, baseInfo)

    image = suv_array[117, :, :]
    plt.figure('PT_000')
    plt.imshow(image, cmap='gray')
    plt.show()




if __name__ == '__main__':
    main()
