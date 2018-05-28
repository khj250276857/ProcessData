import os
import numpy as np
from PIL import Image
from scipy.misc import imsave
import matplotlib.pyplot as plt


# 按照相同子文件目录，将source中文件的每个seris形成20张图象一个cycle，保存在new文件夹中

def main():
    work_dir = r'E:\training data\MR Cardiac\source_validate(16-30)'
    new_work_dir = r'E:\training data\MR Cardiac\new_validate'
    work_spaces = [os.path.join(work_dir, _) for _ in os.listdir(work_dir)]

    for work_space in work_spaces:
        print('processing {}...........'.format(work_space))
        new_work_space = os.path.join(new_work_dir, '{:>02}_new'.format(os.path.split(work_space)[-1]))
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

            print('processing {}'.format(file_paths[i]))
            for num in range(int(len(file_names)/20)):
                path = os.path.join(new_file_paths[i], 'cycle{:>02}'.format(num+1))
                if not os.path.exists(path):
                    os.mkdir(path)
                for _ in range(20*num, 20*num+20):
                    imsave(os.path.join(path, '{:>03}.png'.format(_+1)), img_arrs[_])
    print('processing done')

if __name__ == '__main__':
    main()