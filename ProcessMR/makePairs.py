import os
from PIL import Image
from ProcessMR.gen_all_pairs import main as new_main


#以枚举的方法，将new文件夹中每个cycle的20张图片生成380个训练图像对(fixed和moving文件夹)，保存在pairs文件夹中

def save_image_from_list(save_path, names_list):
    for i in range(len(names_list)):
        img = Image.open(names_list[i]).convert('L')
        img.save(os.path.join(save_path, '{:>05}.png'.format(i+1)))


def main():
    work_dir = r'E:\training data\MR Cardiac(2)\new'
    save_dir = r'E:\training data\MR Cardiac(2)\pairs'
    work_spaces = [os.path.join(work_dir, _) for _ in os.listdir(work_dir)]
    for work_space in work_spaces:
        print('processing {}....................'.format(work_space))

        save_path = os.path.join(save_dir, '{:>02}_pairs'.format(os.path.split(work_space)[-1].split('_')[0]))
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        save_path_x = os.path.join(save_path, 'fixed')
        save_path_y = os.path.join(save_path, 'moving')
        if not os.path.exists(save_path_x):
            os.mkdir(save_path_x)
        if not os.path.exists(save_path_y):
            os.mkdir(save_path_y)

        file_paths = [os.path.join(work_space, _) for _ in os.listdir(work_space)]
        img_name_x = []
        img_name_y = []

        for file_path in file_paths:
            cycle_names = [os.path.join(file_path, _) for _ in os.listdir(file_path)]
            #处理每个cycle
            for cycle_name in cycle_names:
                img_names = [os.path.join(cycle_name, _) for _ in os.listdir(cycle_name)]
                for i in range(len(img_names)):
                    for j in range(len(img_names)):
                        if j == i:
                            continue
                        img_name_x.append(img_names[i])
                        img_name_y.append(img_names[j])
        print('image num: {}'.format(len(img_name_x)))

        print('.........................')
        print('saving images')
        save_image_from_list(save_path_x, img_name_x)
        save_image_from_list(save_path_y, img_name_y)
        print('saving done')


if __name__ == '__main__':
    main()
    new_main()