import pydicom as pdm
import os
import numpy as np
import cv2
import pickle
from scipy.misc import imsave

# 读取文件中所有病人的全部CT图像进行处理，路径：workspace
# 将C图像归一化为0-255，resize为128*128，
#进行平移/旋转，后将array保存至pickle文件，路径：pickle_out_path

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
        imsave(save_path+'/{:>05}.jpg'.format(i+22393), input_array[i])

def main():
    workspace = r'E:\实验数据\workspace_out'
    file_path = [os.path.join(workspace, _) for _ in os.listdir(workspace)]
    ct_file_paths = [os.path.join(_, 'CT') for _ in file_path]
    pt_file_paths = [os.path.join(_, 'PT') for _ in file_path]
    # pickle_out_path = r'E:\实验数据'
    M = np.float32([[1, 0, 10], [0, 1, 10]])  # 平移矩阵（Tx,Ty:X,Y方向移动距离）

    print('Processing {}'.format(ct_file_paths[80]))
    ct_file_names0 = [os.path.join(ct_file_paths[80], _) for _ in os.listdir(ct_file_paths[80])]
    # pt_file_names0 = [os.path.join(pt_file_paths[0], _) for _ in os.listdir(pt_file_paths[0])]
    ct_arrs0 = np.array([pdm.read_file(ct_file_name).pixel_array for ct_file_name in ct_file_names0], dtype='float32')  #512*512
    # pt_arrs0 = np.array([pdm.read_file(pt_file_name).pixel_array for pt_file_name in pt_file_names0], dtype='float32')

    for i in range(ct_arrs0.shape[0]):
        ct_arrs0[i] = np.clip(ct_arrs0[i], 500, ct_arrs0.max())
    normolized_ct_arrs0 = self_normolize(ct_arrs0)
    resized_ct_arrs0 = self_resize(normolized_ct_arrs0)
    shift_ct_arrs0 = shift(resized_ct_arrs0, M)

    # normolized_pt_arrs0 = self_normolize(pt_arrs0)
    # shift_pt_arrs0 = shift(normolized_pt_arrs0, M)

    for ct_file_path in ct_file_paths[81:95]:
        print('Processing {}'.format(ct_file_path))
        ct_file_names = [os.path.join(ct_file_path, _) for _ in os.listdir(ct_file_path)]
        ct_arrs = np.array([pdm.read_file(ct_file_name).pixel_array for ct_file_name in ct_file_names], dtype='float32')
        for i in range(ct_arrs.shape[0]):
            ct_arrs[i] = np.clip(ct_arrs[i], 500, ct_arrs.max())
        normolized_ct_arrs = self_normolize(ct_arrs)
        resized_ct_arrs = self_resize(normolized_ct_arrs)
        shift_ct_arrs = shift(resized_ct_arrs, M)
        resized_ct_arrs0 = np.append(resized_ct_arrs0, resized_ct_arrs, axis=0)
        shift_ct_arrs0 = np.append(shift_ct_arrs0, shift_ct_arrs, axis=0)

    # for pt_file_path in pt_file_paths[81:95]:
    #     print('Processing {}'.format(pt_file_path))
    #     pt_file_names = [os.path.join(pt_file_path, _) for _ in os.listdir(pt_file_path)]
    #     pt_arrs = np.array([pdm.read_file(pt_file_name).pixel_array for pt_file_name in pt_file_names], dtype='float32')
    #     normolized_pt_arrs = self_normolize(pt_arrs)
    #     shift_pt_arrs = shift(normolized_pt_arrs, M)
    #     normolized_pt_arrs0 = np.append(normolized_pt_arrs0, normolized_pt_arrs, axis=0)
    #     shift_pt_arrs0 = np.append(shift_pt_arrs0, shift_pt_arrs, axis=0)

    print('saving resized_ct')
    savespace = r'E:\实验数据\workspace_out_to_image\all_new'
    resized_ct_path = os.path.join(savespace, 'resized_ct')
    if not os.path.exists(resized_ct_path):
        os.mkdir(resized_ct_path)
    save_image_from_array(resized_ct_path, resized_ct_arrs0)

    print('saving shift_ct')
    shift_ct_path = os.path.join(savespace, 'shift_10_10_ct')
    if not os.path.exists(shift_ct_path):
        os.mkdir(shift_ct_path)
    save_image_from_array(shift_ct_path, shift_ct_arrs0)

    # print('saving normolized_pt')
    # savespace = r'E:\实验数据\workspace_out_to_image\all_new'
    # normolized_pt_path = os.path.join(savespace, 'normolized_pt')
    # if not os.path.exists(normolized_pt_path):
    #     os.mkdir(normolized_pt_path)
    # save_image_from_array(normolized_pt_path, normolized_pt_arrs0)
    #
    # print('saving shift_pt')
    # shift_pt_path = os.path.join(savespace, 'shift_10_10_pt')
    # if not os.path.exists(shift_pt_path):
    #     os.mkdir(shift_pt_path)
    # save_image_from_array(shift_pt_path, shift_pt_arrs0)


if __name__ == '__main__':
    main()