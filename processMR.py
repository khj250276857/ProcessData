import os
import numpy as np
from PIL import Image
from scipy.misc import imsave
import matplotlib.pyplot as plt


# img = Image.open(r'E:\MR Cardiac\01\Se1\IMG-0002-00001.bmp')
# img_arr = np.array(img)[:, :, 0]
# plt.figure('img')
# plt.imshow(img_arr, cmap='gray')
# plt.show()


def main():
    work_space = r'E:\MR Cardiac\source\03'
    new_work_space = r'E:\MR Cardiac\new\new_03'
    if not os.path.exists(new_work_space):
        os.mkdir(new_work_space)

    file_paths = [os.path.join(work_space, _) for _ in os.listdir(work_space)]
    # 为目标文件生成子文件
    new_file_paths = [os.path.join(new_work_space, _) for _ in os.listdir(work_space)]
    for new_file_path in new_file_paths:
        if not os.path.exists(new_file_path):
            os.mkdir(new_file_path)

    for i in range(len(file_paths)):
        file_names = [os.path.join(file_paths[i], _) for _ in os.listdir(file_paths[i])]
        img_arrs = np.zeros(shape=(len(file_names), 256, 256))
        for j in range(len(file_names)):
            img = Image.open(file_names[j])
            img_arrs[j] = np.array(img)[:, :, 0]
        print(file_paths[i], ':', img_arrs.shape)

        print('processing {}.................'.format(file_paths[i]))
        for num in range(int(len(file_names)/20)):
            path = os.path.join(new_file_paths[i], 'cycle{:>02}'.format(str(num+1)))
            if not os.path.exists(path):
                os.mkdir(path)
            for _ in range(20*num, 20*num+20):
                imsave(os.path.join(path, str(_+1)+'.png'), img_arrs[_])


if __name__ == '__main__':
    main()