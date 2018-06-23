import pydicom as pdm
import os
import numpy as np
from scipy.misc import imsave
import cv2

def self_resize(input_array):
    output_array = []
    for i in range(input_array.shape[0]):
        output_array.append(cv2.resize(input_array[i], (128, 128), interpolation=cv2.INTER_CUBIC))
    output_array = np.array(output_array, dtype='float32')
    return output_array

def shift(input_array, M):
    output_array = np.copy(input_array)
    slice, rows, cols = output_array.shape
    for i in range(slice):
        output_array[i] = cv2.warpAffine(output_array[i], M, (rows, cols))
    return output_array

def rotate(input_array, N):
    output_array = np.copy(input_array)
    slice, rows, cols = output_array.shape
    for i in range(slice):
        output_array[i] = cv2.warpAffine(output_array[i], N, (rows, cols))
    return output_array

def save_image_from_array(save_path, input_array):
    for i in range(input_array.shape[0]):
        imsave(save_path+'/{:>05}.jpg'.format(i+1), input_array[i])


def main():
    workspace = r'E:\实验数据\workspace_out\PT00704-5'
    ct_workspace = os.path.join(workspace, 'CT')
    # pt_workspace = os.path.join(workspace, 'PT')
    ct_file_paths = [os.path.join(ct_workspace, _) for _ in os.listdir(ct_workspace)]
    # pt_file_paths = [os.path.join(pt_workspace, _) for _ in os.listdir(pt_workspace)]
    ct_arrs = np.array([pdm.read_file(ct_file_path).pixel_array for ct_file_path in ct_file_paths], dtype='float32')    # 512*512
    # pt_arrs = np.array([pdm.read_file(pt_file_path).pixel_array for pt_file_path in pt_file_paths], dtype='float32')

    for i in range(ct_arrs.shape[0]):
        ct_arrs[i] = np.clip(ct_arrs[i], 500, ct_arrs.max())

    resized_ct_arrs = self_resize(ct_arrs)  # 128*128
    slice, rows, cols = resized_ct_arrs.shape

    M = np.float32([[1, 0, 10], [0, 1, 10]])  # 平移矩阵（Tx,Ty:X,Y方向移动距离），当前为向右下移动10个像素
    N = cv2.getRotationMatrix2D((cols / 2, rows / 2), 45, 1)  # 旋转矩阵(旋转中心点，旋转角度，缩放比例)，当前为旋转45度
    shift_ct_arrs = shift(resized_ct_arrs, M)
    # shift_pt_arrs = shift(pt_arrs, M)
    rotate_ct_arrs = rotate(resized_ct_arrs, N)
    # rotate_pt_arrs = rotate(pt_arrs, N)

    print('saving resized_ct')
    savespace = r'E:\实验数据\workspace_out_to_image\PT00704-5'
    resized_ct_path = os.path.join(savespace, 'resized_ct')
    if not os.path.exists(resized_ct_path):
        os.mkdir(resized_ct_path)
    save_image_from_array(resized_ct_path, resized_ct_arrs)

    print('saving shift_ct')
    shift_ct_path = os.path.join(savespace, 'shift_10_10_ct')
    if not os.path.exists(shift_ct_path):
        os.mkdir(shift_ct_path)
    save_image_from_array(shift_ct_path, shift_ct_arrs)

    print('saving rotate_ct')
    rotate_ct_path = os.path.join(savespace, 'rotate_45_ct')
    if not os.path.exists(rotate_ct_path):
        os.mkdir(rotate_ct_path)
    save_image_from_array(rotate_ct_path, rotate_ct_arrs)

    # savespace = r'E:\实验数据\workspace_out_to_image\PT00704-5'
    # print('saving pt')
    # pt_path = os.path.join(savespace, 'pt')
    # if not os.path.exists(pt_path):
    #     os.mkdir(pt_path)
    # save_image_from_array(pt_path, pt_arrs)
    #
    # print('saving shift_pt')
    # shift_pt_path = os.path.join(savespace, 'shift_10_10_pt')
    # if not os.path.exists(shift_pt_path):
    #     os.mkdir(shift_pt_path)
    # save_image_from_array(shift_pt_path, shift_pt_arrs)
    #
    # print('saving rotate_pt')
    # rotate_pt_path = os.path.join(savespace, 'rotate_45_pt')
    # if not os.path.exists(rotate_pt_path):
    #     os.mkdir(rotate_pt_path)
    # save_image_from_array(rotate_pt_path, rotate_pt_arrs)

if __name__ == '__main__':
    main()