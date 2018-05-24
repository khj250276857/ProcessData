import os
import numpy as np
from PIL import Image
from scipy.misc import imsave

def save_image_from_array(save_path, input_array):
    for i in range(input_array.shape[0]):
        imsave(save_path+'/{:>04}.png'.format(i+1), input_array[i])

def main():
    workspace = r'E:\MR Cardiac\new\new_03'
    save_path = r'E:\MR Cardiac\pairs\03_pairs'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path_x = os.path.join(save_path, 'fixed')
    save_path_y = os.path.join(save_path, 'moving')
    if not os.path.exists(save_path_x):
        os.mkdir(save_path_x)
    if not os.path.exists(save_path_y):
        os.mkdir(save_path_y)

    file_paths = [os.path.join(workspace, _) for _ in os.listdir(workspace)]
    img_arrs_x = np.zeros([1, 256, 256], dtype='float32')
    img_arrs_y = np.zeros([1, 256, 256], dtype='float32')

    for file_path in file_paths:
        cycle_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
        #处理每个cycle
        for cycle_name in cycle_names:
            print('processing {}......'.format(cycle_name))
            img_names = [os.path.join(cycle_name, _) for _ in os.listdir(cycle_name)]
            img_arrs_x_temp = np.zeros([1, 256, 256])
            img_arrs_y_temp = np.zeros([1, 256, 256])

            for i in range(len(os.listdir(cycle_name))):
                for j in range(i+1, len(os.listdir(cycle_name))):
                    img_x = np.array(Image.open(img_names[i]))
                    img_y = np.array(Image.open(img_names[j]))
                    img_x = img_x.reshape(1, img_x.shape[0], img_x.shape[1])
                    img_y = img_y.reshape(1, img_y.shape[0], img_y.shape[1])
                    img_arrs_x_temp = np.append(img_arrs_x_temp, img_x, axis=0)
                    img_arrs_y_temp = np.append(img_arrs_y_temp, img_y, axis=0)
            img_arrs_x_temp = img_arrs_x_temp[1:img_arrs_x_temp.shape[0], :, :]
            img_arrs_y_temp = img_arrs_y_temp[1:img_arrs_y_temp.shape[0], :, :]
            img_arrs_x = np.append(img_arrs_x, img_arrs_x_temp, axis=0)
            img_arrs_y = np.append(img_arrs_y, img_arrs_y_temp, axis=0)
            print(img_arrs_x.shape)

    img_arrs_x = img_arrs_x[1:img_arrs_x.shape[0], :, :]
    img_arrs_y = img_arrs_y[1:img_arrs_y.shape[0], :, :]
    print('.........................')
    print('saving images')
    save_image_from_array(save_path_x, img_arrs_x)
    save_image_from_array(save_path_y, img_arrs_y)
    print('saving done')


if __name__ == '__main__':
    main()