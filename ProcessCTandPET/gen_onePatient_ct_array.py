import pydicom as pdm
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import io
import pickle

def self_normolize(input_array):
    max_pixel = input_array.max()
    min_pixel = input_array.min()
    for i in range(input_array.shape[0]):
        input_array[i] = (input_array[i]-min_pixel)/(max_pixel-min_pixel)*255
    return input_array

def self_resize(input_array):
    output_array = []
    for i in range(input_array.shape[0]):
        output_array.append(cv2.resize(input_array[i], (128, 128), interpolation=cv2.INTER_CUBIC))
    output_array = np.array(output_array, dtype='float32')
    return output_array

def shift(input_array, M):
    slice, rows, cols = input_array.shape
    for i in range(slice):
        input_array[i] = cv2.warpAffine(input_array[i], M, (rows, cols))
    return input_array

def main():
    workspace = r'E:\实验数据\workspace_out\PT00704-5'
    ct_workspace = os.path.join(workspace, 'CT')
    ct_out_workspace = os.path.join(workspace, 'CT_out')
    if not os.path.exists(ct_out_workspace):
        os.mkdir(ct_out_workspace)
    ct_file_paths = [os.path.join(ct_workspace, _) for _ in os.listdir(ct_workspace)]

    ct_arrs = np.array([pdm.read_file(ct_file).pixel_array for ct_file in ct_file_paths], dtype='float32')  # 512*512
    normolized_ct_arrs = self_normolize(ct_arrs)
    resized_ct_arrs = self_resize(normolized_ct_arrs)  # 128*128

    M = np.float32([[1, 0, -10], [0, 1, -10]])  # 平移矩阵
    shift_ct_arrs = shift(resized_ct_arrs, M)
    # resized_ct_arrs = resized_ct_arrs[:, :, :, np.newaxis]
    # shift_ct_arrs = shift_ct_arrs[:, :, :, np.newaxis]


    # with open(ct_out_workspace+'/shift10.pkl', 'wb') as f:
    #     pickle.dump((resized_ct_arrs, shift_ct_arrs), f)

    plt.figure('before')
    plt.imshow(resized_ct_arrs[100], cmap='gray')
    plt.figure('after')
    plt.imshow(shift_ct_arrs[100], cmap='gray')
    plt.show()


if __name__ == '__main__':
    main()



